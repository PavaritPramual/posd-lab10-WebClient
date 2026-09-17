package com.example.lab10;

import com.example.lab10.client.ProductWebClient;
import com.example.lab10.model.Product;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import reactor.test.StepVerifier;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class ProductWebClientIntegrationTests {

    @LocalServerPort
    private int port;

    private ProductWebClient client;

    @BeforeEach
    void setUp() {
        client = new ProductWebClient("http://localhost:" + port);
    }

    @Test
    void webClientCallsEveryEndpointWithoutBlocking() {
        Product product = new Product("webclient-test", "USB-C Hub", "Accessories",
                "Anker", 15, 2000.0, "SEASONAL");

        StepVerifier.create(client.getAllProducts().collectList())
                .assertNext(products -> assertThat(products).hasSizeGreaterThanOrEqualTo(3))
                .verifyComplete();

        StepVerifier.create(client.createProduct(product)
                        .flatMap(saved -> client.getProductById(saved.getId())))
                .assertNext(saved -> assertThat(saved.getName()).isEqualTo("USB-C Hub"))
                .verifyComplete();

        StepVerifier.create(client.getByCategory("Accessories").collectList())
                .assertNext(products -> assertThat(products)
                        .anyMatch(item -> "webclient-test".equals(item.getId())))
                .verifyComplete();

        StepVerifier.create(client.getDiscountedPrice("webclient-test"))
                .expectNext(1600.0)
                .verifyComplete();

        StepVerifier.create(client.deleteProduct("webclient-test"))
                .verifyComplete();

        StepVerifier.create(client.getProductById("webclient-test")
                        .map(Product::getName)
                        .defaultIfEmpty("Product not found"))
                .expectNext("Product not found")
                .verifyComplete();
    }
}
