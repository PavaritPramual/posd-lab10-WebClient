# Lab 10: Spring WebFlux และ WebClient

ระบบ REST API สำหรับจัดการสินค้าแบบ Non-blocking Reactive Programming

- ผู้จัดทำ: นายปวริศช์ ประมวล
- รหัสนักศึกษา: 673380278-9
- Section: 1
- วิชา: CP353002 Principles of Software Design

## เทคโนโลยี

- Java 17+
- Spring Boot 3.3.0
- Spring WebFlux และ Reactor Netty
- Project Reactor (`Mono` และ `Flux`)
- WebClient
- JUnit 5, StepVerifier และ WebTestClient

โปรเจกต์ใช้ `ConcurrentHashMap` เป็น in-memory storage เพื่อเน้นการฝึก Reactive Programming จึงไม่ต้องติดตั้งฐานข้อมูล ข้อมูลจะกลับเป็นค่าเริ่มต้นทุกครั้งที่เริ่มแอปใหม่

## โครงสร้างและ Reactive Operators

การไหลของข้อมูลคือ `Controller -> Service -> Repository` และทุกชั้นคืน `Mono` หรือ `Flux` โดยตรง

- Repository ใช้ `Mono.defer`, `Mono.justOrEmpty`, `Mono.fromSupplier`, `Mono.fromRunnable`, `Flux.defer` และ `filter`
- Service ใช้ `map`, `flatMap` และ `switchIfEmpty`
- Controller คืน publisher ให้ Spring WebFlux subscribe เมื่อส่ง HTTP response
- WebClient คืน publisher ให้ caller chain operator ต่อได้ โดยไม่มี `.block()` ใน production code

## Endpoints

| Method | URL | Return type | รายละเอียด |
|---|---|---|---|
| GET | `/products` | `Flux<Product>` | ดูสินค้าทั้งหมด |
| GET | `/products/{id}` | `Mono<Product>` | ดูสินค้าตาม ID; ไม่พบคืน 404 |
| POST | `/products` | `Mono<Product>` | สร้างสินค้า; สร้าง UUID ให้อัตโนมัติเมื่อไม่ส่ง ID |
| DELETE | `/products/{id}` | `Mono<Void>` | ลบสินค้า; สำเร็จคืน 204 |
| GET | `/products/category/{category}` | `Flux<Product>` | กรอง category แบบไม่สนตัวพิมพ์ใหญ่เล็ก |
| GET | `/products/{id}/price` | `Mono<Double>` | ราคาหลังส่วนลด |

ส่วนลดที่รองรับ:

- `NONE`: ราคาเดิม
- `MEMBER`: ลด 10%
- `SEASONAL`: ลด 20%

## วิธี Clone, Build และ Run

```powershell
git clone https://github.com/PavaritPramual/posd-lab10-WebClient.git
cd posd-lab10-WebClient
mvn clean test
mvn spring-boot:run
```

เมื่อแอปพร้อมใช้งาน ให้เปิด `http://localhost:8080/products`

ถ้า Maven ใน Windows แจ้ง `Could not create local repository at C:\.m2\repository` ให้ระบุ cache ที่เขียนได้:

```powershell
mvn "-Dmaven.repo.local=$PWD\target\m2-repository" test
mvn "-Dmaven.repo.local=$PWD\target\m2-repository" spring-boot:run
```

## ตัวอย่าง Request

สร้างสินค้า:

```powershell
$body = @{
  name = "Mechanical Keyboard"
  category = "Accessories"
  brand = "Keychron"
  stock = 10
  price = 3500.0
  discountType = "MEMBER"
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri http://localhost:8080/products `
  -ContentType application/json `
  -Body $body
```

ค้นหาตาม category และดูราคาหลังส่วนลด:

```powershell
Invoke-RestMethod http://localhost:8080/products/category/Electronics
Invoke-RestMethod http://localhost:8080/products/1/price
```

## WebClient และ Operator Chain

`ProductWebClient` เรียก REST API โดยไม่บล็อก thread และคืน publisher ให้ chain ต่อได้ทันที:

```java
productWebClient.getProductById("1")
    .map(Product::getName)
    .defaultIfEmpty("Product not found")
    .subscribe(System.out::println);
```

ใน server code ไม่เรียก `subscribe()` เอง เพราะ Spring WebFlux เป็นผู้ subscribe publisher เมื่อมี HTTP request ส่วนตัวอย่างข้างบนเป็นการ subscribe ที่ขอบระบบฝั่ง consumer เท่านั้น

## การทดสอบ

```powershell
mvn "-Dmaven.repo.local=$PWD\target\m2-repository" test
mvn "-Dmaven.repo.local=$PWD\target\m2-repository" package
```

ชุดทดสอบครอบคลุม:

- Repository และ Service ด้วย StepVerifier
- การค้นหา บันทึก ลบ กรอง category และคำนวณส่วนลด
- REST API ทุก endpoint ด้วย WebTestClient
- ProductWebClient ที่เรียก Reactor Netty server จริงบน random port
- chain `.map().defaultIfEmpty()` เมื่อสินค้าไม่พบ

ผลที่คาดหวัง: `Tests run: 10, Failures: 0, Errors: 0, Skipped: 0` และ `BUILD SUCCESS`

## Screenshots และรายงาน

- Screenshot output จริงจาก `curl.exe -i`: [`screenshots`](screenshots)
- รายงาน PDF: [`Lab10_673380278-9Sec1.pdf`](Lab10_673380278-9Sec1.pdf)

## Troubleshooting

- Port 8080 ถูกใช้งาน: ปิด process เดิม หรือแก้ `server.port` และ `product.api.base-url` ให้ตรงกัน
- ได้ 404: ตรวจ ID จาก `GET /products` ก่อนเรียก endpoint รายการเดียว
- ข้อมูลที่สร้างหายหลัง restart: เป็นพฤติกรรมปกติของ in-memory repository
- WebClient ต่อไม่ได้: ตรวจว่า server ทำงานและ base URL ชี้ไปยัง port ที่ถูกต้อง
