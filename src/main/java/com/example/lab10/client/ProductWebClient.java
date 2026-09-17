package com.example.lab10.client;

import com.example.lab10.model.Product;
import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * ProductWebClient — Reactive HTTP Client
 *
 * เรียก Product API แบบ non-blocking และคืน Mono/Flux ให้ caller chain ต่อได้
 *
 * WebClient method chain:
 *   client.get()              ← HTTP method
 *     .uri("/products/{id}", id)  ← URL
 *     .retrieve()             ← เริ่มรับ response
 *     .bodyToMono(T.class)    ← แปลงเป็น Mono<T>
 *     .bodyToFlux(T.class)    ← แปลงเป็น Flux<T>
 */
@Component
public class ProductWebClient {

    private final WebClient client;

    public ProductWebClient(@Value("${product.api.base-url:http://localhost:8080}") String baseUrl) {
        this.client = WebClient.create(baseUrl);
    }

    /**
     * GET /products/{id} → Mono<Product>
     * ดึง Product 1 รายการจาก server
     */
    public Mono<Product> getProductById(String id) {
        return client.get()
                .uri("/products/{id}", id)
                .retrieve()
                .bodyToMono(Product.class)
                .onErrorResume(WebClientResponseException.NotFound.class,
                        error -> Mono.empty());
    }

    /**
     * GET /products → Flux<Product>
     * ดึง Product ทั้งหมดจาก server
     *
     * Hint: client.get()
     *         .uri("/products")
     *         .retrieve()
     *         .bodyToFlux(Product.class)
     */
    public Flux<Product> getAllProducts() {
        return client.get()
                .uri("/products")
                .retrieve()
                .bodyToFlux(Product.class);
    }

    /**
     * POST /products → Mono<Product>
     * ส่ง Product ใหม่ไปยัง server
     *
     * Hint: client.post()
     *         .uri("/products")
     *         .bodyValue(product)   ← ส่ง body
     *         .retrieve()
     *         .bodyToMono(Product.class)
     */
    public Mono<Product> createProduct(Product product) {
        return client.post()
                .uri("/products")
                .bodyValue(product)
                .retrieve()
                .bodyToMono(Product.class);
    }

    /**
     * DELETE /products/{id} → Mono<Void>
     * ส่ง request ลบ Product
     *
     * Hint: client.delete()
     *         .uri("/products/{id}", id)
     *         .retrieve()
     *         .bodyToMono(Void.class)
     */
    public Mono<Void> deleteProduct(String id) {
        return client.delete()
                .uri("/products/{id}", id)
                .retrieve()
                .bodyToMono(Void.class);
    }

    /**
     * GET /products/category/{category} → Flux<Product>
     * ดึง Product ตาม category
     *
     * Hint: client.get()
     *         .uri("/products/category/{category}", category)
     *         .retrieve()
     *         .bodyToFlux(Product.class)
     */
    public Flux<Product> getByCategory(String category) {
        return client.get()
                .uri("/products/category/{category}", category)
                .retrieve()
                .bodyToFlux(Product.class);
    }

    /**
     * GET /products/{id}/price → Mono<Double>
     * ดึงราคาหลังส่วนลด
     *       แล้ว chain .doOnNext() เพื่อ log ราคาที่ได้
     *
     * Hint: client.get()
     *         .uri("/products/{id}/price", id)
     *         .retrieve()
     *         .bodyToMono(Double.class)
     *         .doOnNext(price -> System.out.println("Price: " + price))
     */
    public Mono<Double> getDiscountedPrice(String id) {
        return client.get()
                .uri("/products/{id}/price", id)
                .retrieve()
                .bodyToMono(Double.class)
                .doOnNext(price -> System.out.println("Price: " + price));
    }
}
