package com.example.lab10.controller;

import com.example.lab10.model.Product;
import com.example.lab10.service.ProductService;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.HttpStatus;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * ProductController — Reactive REST Controller
 *
 * Reactive endpoints ครบทุก use case ของ Product
 *
 * Endpoints ที่ต้องทำทั้งหมด:
 *   GET    /products          → Flux<Product>   (ดึงทั้งหมด)
 *   GET    /products/{id}     → Mono<Product>
 *   POST   /products          → Mono<Product>   (บันทึก)
 *   DELETE /products/{id}     → Mono<Void>      (ลบ)
 *   GET    /products/category/{cat} → Flux<Product> (กรอง)
 *   GET    /products/{id}/price    → Mono<Double>   (ราคาหลังลด)
 */
@RestController
@RequestMapping("/products")
public class ProductController {

    // ── Constructor Injection (DIP — SOLID) ─────────────
    private final ProductService service;

    public ProductController(ProductService service) {
        this.service = service;
    }

    /**
     * GET /products/{id}
     * คืน Mono<Product> — ค้นหา Product 1 รายการ
     *
     * ทดสอบ: GET http://localhost:8080/products/1
     */
    @GetMapping("/{id}")
    public Mono<Product> getById(@PathVariable String id) {
        return service.getById(id);
    }

    /**
     * GET /products
     * คืน Flux<Product> ทุกรายการ
     *
     * Hint: เรียก service.getAll()
     * ทดสอบ: GET http://localhost:8080/products
     */
    @GetMapping
    public Flux<Product> getAll() {
        return service.getAll();
    }

    /**
     * POST /products
     * รับ Product จาก request body แล้วบันทึก
     *
     * Hint: เรียก service.save(product)
     * ทดสอบ: POST http://localhost:8080/products
     *        Body: { "name": "...", "price": 999.0, ... }
     */
    @PostMapping
    public Mono<Product> save(@RequestBody Product product) {
        return service.save(product);
    }

    /**
     * DELETE /products/{id}
     * ลบ Product และคืน Mono<Void>
     *
     * Hint: เรียก service.delete(id)
     * ทดสอบ: DELETE http://localhost:8080/products/1
     */
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> delete(@PathVariable String id) {
        return service.delete(id);
    }

    /**
     * GET /products/category/{category}
     * คืน Flux<Product> ที่กรองตาม category
     *
     * Hint: เรียก service.getByCategory(category)
     * ทดสอบ: GET http://localhost:8080/products/category/Electronics
     */
    @GetMapping("/category/{category}")
    public Flux<Product> getByCategory(@PathVariable String category) {
        return service.getByCategory(category);
    }

    /**
     * GET /products/{id}/price
     * คืน Mono<Double> ราคาหลังส่วนลด
     *
     * Hint: เรียก service.getDiscountedPrice(id)
     * ทดสอบ: GET http://localhost:8080/products/1/price
     */
    @GetMapping("/{id}/price")
    public Mono<Double> getDiscountedPrice(@PathVariable String id) {
        return service.getDiscountedPrice(id);
    }
}
