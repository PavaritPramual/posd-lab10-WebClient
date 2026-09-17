package com.example.lab10.service;

import com.example.lab10.model.Product;
import com.example.lab10.repository.ProductRepository;
import org.springframework.stereotype.Service;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.UUID;

/**
 * ProductService — Business Logic Layer
 *
 * ใช้ Constructor Injection ตามหลัก DIP และประกอบ reactive operators
 *
 * หน้าที่: รับ request จาก Controller → เรียก Repository → คืนผล
 * (SRP — แต่ละ class มีหน้าที่เดียว)
 *
 * Hint Operators ที่ควรใช้:
 *   .map(p -> ...)            แปลงค่า
 *   .flatMap(p -> ...)        async transform
 *   .defaultIfEmpty(...)      fallback ถ้าว่าง
 *   .switchIfEmpty(Mono...)   fallback Mono ถ้าว่าง
 */
@Service
public class ProductService {

    // ── Constructor Injection (DIP — SOLID) ─────────────
    private final ProductRepository repository;

    public ProductService(ProductRepository repository) {
        this.repository = repository;
    }

    // ── 1. ดึง Product 1 รายการ ──────────────────────────
    /**
     * เรียก repository.findById(id) แล้วคืนผล
     *       ถ้าไม่พบให้ throw RuntimeException("Product not found: " + id)
     *
     * Hint: repository.findById(id)
     *       .switchIfEmpty(Mono.error(new RuntimeException(...)))
     */
    public Mono<Product> getById(String id) {
        return repository.findById(id)
                .switchIfEmpty(Mono.error(new ResponseStatusException(
                        HttpStatus.NOT_FOUND, "Product not found: " + id)));
    }

    // ── 2. ดึง Product ทั้งหมด ───────────────────────────
    /**
     * เรียก repository.findAll() แล้วคืนผล
     */
    public Flux<Product> getAll() {
        return repository.findAll();
    }

    // ── 3. บันทึก Product ────────────────────────────────
    /**
     * เรียก repository.save(product) แล้วคืนผล
     *
     * เพิ่มเติม: ถ้า product.getId() เป็น null ให้ generate id ใหม่
     * Hint: java.util.UUID.randomUUID().toString()
     */
    public Mono<Product> save(Product product) {
        return Mono.just(product)
                .map(item -> {
                    if (item.getId() == null || item.getId().isBlank()) {
                        item.setId(UUID.randomUUID().toString());
                    }
                    return item;
                })
                .flatMap(repository::save);
    }

    // ── 4. ลบ Product ────────────────────────────────────
    /**
     * เรียก repository.deleteById(id) แล้วคืนผล
     */
    public Mono<Void> delete(String id) {
        return getById(id)
                .flatMap(product -> repository.deleteById(id));
    }

    // ── 5. กรองตาม category ──────────────────────────────
    /**
     * เรียก repository.findByCategory(category) แล้วคืนผล
     */
    public Flux<Product> getByCategory(String category) {
        return repository.findByCategory(category);
    }

    // ── 6. คำนวณราคาหลังส่วนลด ───────────────────────────
    /**
     * หา Product จาก id แล้วคืน discountedPrice
     *
     * Hint: getById(id)
     *       .map(p -> p.getDiscountedPrice())
     */
    public Mono<Double> getDiscountedPrice(String id) {
        return getById(id)
                .map(Product::getDiscountedPrice);
    }
}
