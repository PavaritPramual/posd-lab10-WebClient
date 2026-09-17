package com.example.lab10;

import com.example.lab10.model.Product;
import com.example.lab10.repository.ProductRepository;
import com.example.lab10.service.ProductService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.web.server.ResponseStatusException;
import reactor.test.StepVerifier;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
class Lab10ApplicationTests {

    private ProductRepository repository;
    private ProductService service;

    @BeforeEach
    void setUp() {
        repository = new ProductRepository();
        service = new ProductService(repository);
    }

    @Test
    void contextLoads() {
    }

    @Test
    void findByIdReturnsProductAndCompletesEmptyWhenMissing() {
        StepVerifier.create(repository.findById("1"))
                .assertNext(product -> {
                    assertThat(product.getName()).contains("นายปวริศช์ ประมวล");
                    assertThat(product.getName()).contains("673380278-9");
                })
                .verifyComplete();

        StepVerifier.create(repository.findById("999"))
                .verifyComplete();
    }

    @Test
    void findAllReturnsSeedProducts() {
        StepVerifier.create(repository.findAll().collectList())
                .assertNext(products -> assertThat(products).hasSize(3))
                .verifyComplete();
    }

    @Test
    void saveAndDeleteAreDeferredReactiveOperations() {
        Product product = new Product("test-1", "Keyboard", "Accessories",
                "Keychron", 8, 3490.0, "NONE");

        StepVerifier.create(repository.save(product).flatMap(saved -> repository.findById(saved.getId())))
                .expectNext(product)
                .verifyComplete();

        StepVerifier.create(repository.deleteById(product.getId())
                        .then(repository.findById(product.getId())))
                .verifyComplete();
    }

    @Test
    void categoryFilterIgnoresCase() {
        StepVerifier.create(repository.findByCategory("electronics").collectList())
                .assertNext(products -> assertThat(products)
                        .hasSize(3)
                        .allMatch(product -> "Electronics".equals(product.getCategory())))
                .verifyComplete();
    }

    @Test
    void serviceGeneratesIdAndUsesFlatMapToSave() {
        Product product = new Product(null, "Mouse", "Accessories",
                "Logitech", 12, 1290.0, "NONE");

        StepVerifier.create(service.save(product))
                .assertNext(saved -> {
                    assertThat(saved.getId()).isNotBlank();
                    assertThat(saved.getName()).isEqualTo("Mouse");
                })
                .verifyComplete();
    }

    @Test
    void serviceReturnsNotFoundError() {
        StepVerifier.create(service.getById("missing"))
                .expectErrorSatisfies(error -> {
                    assertThat(error).isInstanceOf(ResponseStatusException.class);
                    assertThat(((ResponseStatusException) error).getStatusCode().value()).isEqualTo(404);
                })
                .verify();
    }

    @Test
    void discountedPricesCoverAllDiscountTypes() {
        StepVerifier.create(service.getDiscountedPrice("1"))
                .expectNext(35910.0)
                .verifyComplete();
        StepVerifier.create(service.getDiscountedPrice("2"))
                .expectNext(49900.0)
                .verifyComplete();
        StepVerifier.create(service.getDiscountedPrice("3"))
                .expectNext(23920.0)
                .verifyComplete();
    }
}
