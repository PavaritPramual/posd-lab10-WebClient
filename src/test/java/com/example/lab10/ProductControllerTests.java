package com.example.lab10;

import com.example.lab10.model.Product;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.reactive.AutoConfigureWebTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.reactive.server.WebTestClient;

@SpringBootTest
@AutoConfigureWebTestClient
class ProductControllerTests {

    @Autowired
    private WebTestClient webTestClient;

    @Test
    void allEndpointsReturnExpectedResponses() {
        webTestClient.get().uri("/products")
                .exchange()
                .expectStatus().isOk()
                .expectBodyList(Product.class).hasSize(3);

        webTestClient.get().uri("/products/1")
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.name").value(name ->
                        org.assertj.core.api.Assertions.assertThat(name.toString())
                                .contains("673380278-9"));

        Product product = new Product("api-test", "Reactive Keyboard", "Accessories",
                "Keychron", 10, 3500.0, "MEMBER");

        webTestClient.post().uri("/products")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(product)
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.id").isEqualTo("api-test");

        webTestClient.get().uri("/products/category/Accessories")
                .exchange()
                .expectStatus().isOk()
                .expectBodyList(Product.class).hasSize(1);

        webTestClient.get().uri("/products/api-test/price")
                .exchange()
                .expectStatus().isOk()
                .expectBody(Double.class).isEqualTo(3150.0);

        webTestClient.delete().uri("/products/api-test")
                .exchange()
                .expectStatus().isNoContent()
                .expectBody().isEmpty();

        webTestClient.get().uri("/products/api-test")
                .exchange()
                .expectStatus().isNotFound();
    }
}
