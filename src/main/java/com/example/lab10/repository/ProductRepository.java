package com.example.lab10.repository;

import com.example.lab10.model.Product;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * ProductRepository — In-memory Reactive Repository
 *
 * ทุก operation คืนค่าเป็น Mono/Flux และไม่บล็อก thread
 *
 * ใช้ ConcurrentHashMap เป็น in-memory storage
 * (ไม่ต่อ Database — เน้นฝึก Mono/Flux)
 *
 * Hint:
 *   - Mono.just(value)          คืนค่าเดียว
 *   - Mono.empty()              คืนเปล่า
 *   - Flux.fromIterable(list)   คืนหลายค่าจาก collection
 */
public class ProductRepository {

    // ── In-memory storage ────────────────────────────────
    private final Map<String, Product> store = new ConcurrentHashMap<>();

    // ── Constructor: ใส่ข้อมูลตัวอย่าง ──────────────────
    public ProductRepository() {
        store.put("1", new Product("1", "iPhone 15 Pro (นายปวริศช์ ประมวล 673380278-9 SEC 1)",
                "Electronics", "Apple", 50, 39900.0, "MEMBER"));
        store.put("2", new Product("2", "MacBook Air M3",
                "Electronics", "Apple", 20, 49900.0, "NONE"));
        store.put("3", new Product("3", "Samsung Galaxy S24",
                "Electronics", "Samsung", 30, 29900.0, "SEASONAL"));
    }

    // ── 1. หา Product 1 รายการ ───────────────────────────
    /**
     * คืน Mono<Product> จาก store โดยใช้ id
     *       ถ้าไม่พบให้คืน Mono.empty()
     *
     * Hint: store.get(id) คืน Product หรือ null
     *       ถ้า null ให้ใช้ Mono.empty()
     *       ถ้ามีค่าให้ใช้ Mono.just(product)
     */
    public Mono<Product> findById(String id) {
        return Mono.defer(() -> Mono.justOrEmpty(store.get(id)));
    }

    // ── 2. หา Product ทั้งหมด ────────────────────────────
    /**
     * คืน Flux<Product> ของทุกรายการใน store
     *
     * Hint: store.values() คืน Collection<Product>
     *       ใช้ Flux.fromIterable(...) แปลงเป็น Flux
     */
    public Flux<Product> findAll() {
        return Flux.defer(() -> Flux.fromIterable(store.values()));
    }

    // ── 3. บันทึก Product ────────────────────────────────
    /**
     * บันทึก product ลง store แล้วคืน Mono<Product>
     *
     * Hint: store.put(product.getId(), product)
     *       แล้วใช้ Mono.just(product) คืนค่า
     */
    public Mono<Product> save(Product product) {
        return Mono.fromSupplier(() -> {
            store.put(product.getId(), product);
            return product;
        });
    }

    // ── 4. ลบ Product ────────────────────────────────────
    /**
     * ลบ product จาก store แล้วคืน Mono<Void>
     *
     * Hint: store.remove(id)
     *       แล้วใช้ Mono.empty() คืนค่า (Mono<Void>)
     */
    public Mono<Void> deleteById(String id) {
        return Mono.fromRunnable(() -> store.remove(id));
    }

    // ── 5. กรองตาม category ──────────────────────────────
    /**
     * คืน Flux<Product> ที่ category ตรงกัน
     *
     * Hint: findAll()
     *       .filter(p -> p.getCategory().equalsIgnoreCase(category))
     */
    public Flux<Product> findByCategory(String category) {
        return findAll()
                .filter(product -> category.equalsIgnoreCase(product.getCategory()));
    }
}
