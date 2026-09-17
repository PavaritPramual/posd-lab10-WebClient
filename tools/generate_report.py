from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Lab10_673380278-9Sec1.pdf"
EVIDENCE = ROOT / "docs" / "evidence"

pdfmetrics.registerFont(TTFont("Tahoma", r"C:\Windows\Fonts\tahoma.ttf"))
pdfmetrics.registerFont(TTFont("Tahoma-Bold", r"C:\Windows\Fonts\tahomabd.ttf"))

BLUE = colors.HexColor("#2563EB")
NAVY = colors.HexColor("#0F172A")
SLATE = colors.HexColor("#475569")
LIGHT = colors.HexColor("#EFF6FF")
GREEN = colors.HexColor("#15803D")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
    canvas.line(20 * mm, 15 * mm, 190 * mm, 15 * mm)
    canvas.setFont("Tahoma", 8)
    canvas.setFillColor(SLATE)
    canvas.drawString(20 * mm, 10 * mm, "LAB10 Spring WebFlux + WebClient | นายปวริศช์ ประมวล 673380278-9")
    canvas.drawRightString(190 * mm, 10 * mm, f"หน้า {doc.page}")
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="ThaiTitle", fontName="Tahoma-Bold", fontSize=27, leading=36,
                          alignment=TA_CENTER, textColor=NAVY, spaceAfter=12))
styles.add(ParagraphStyle(name="ThaiSubtitle", fontName="Tahoma", fontSize=15, leading=23,
                          alignment=TA_CENTER, textColor=SLATE, spaceAfter=10))
styles.add(ParagraphStyle(name="H1Thai", fontName="Tahoma-Bold", fontSize=19, leading=27,
                          textColor=BLUE, spaceBefore=4, spaceAfter=9))
styles.add(ParagraphStyle(name="H2Thai", fontName="Tahoma-Bold", fontSize=13, leading=20,
                          textColor=NAVY, spaceBefore=7, spaceAfter=5))
styles.add(ParagraphStyle(name="BodyThai", fontName="Tahoma", fontSize=10.5, leading=17,
                          textColor=NAVY, spaceAfter=7))
styles.add(ParagraphStyle(name="SmallThai", fontName="Tahoma", fontSize=8.5, leading=13,
                          textColor=SLATE, spaceAfter=4))
styles.add(ParagraphStyle(name="CaptionThai", fontName="Tahoma", fontSize=8.5, leading=12,
                          alignment=TA_CENTER, textColor=SLATE, spaceAfter=8))
code_style = ParagraphStyle(name="CodeThai", fontName="Tahoma", fontSize=7.8, leading=11,
                            textColor=NAVY, leftIndent=7, rightIndent=7,
                            borderPadding=8, backColor=colors.HexColor("#F1F5F9"),
                            borderColor=colors.HexColor("#CBD5E1"), borderWidth=0.6,
                            spaceBefore=5, spaceAfter=8)


def p(text, style="BodyThai"):
    return Paragraph(text, styles[style])


def code(text):
    return Preformatted(text.strip(), code_style)


def evidence_image(name, caption):
    img = Image(str(EVIDENCE / name), width=170 * mm, height=95.625 * mm)
    return [img, p(caption, "CaptionThai")]


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=22 * mm,
        title="Lab 10 Spring WebFlux and WebClient",
        author="นายปวริศช์ ประมวล 673380278-9",
    )
    story = []

    story += [Spacer(1, 30 * mm), p("รายงานปฏิบัติการที่ 10", "ThaiTitle"),
              p("Spring WebFlux และ WebClient", "ThaiTitle"), Spacer(1, 8 * mm),
              p("ระบบ REST API จัดการสินค้าแบบ Non-blocking Reactive Programming", "ThaiSubtitle"),
              Spacer(1, 20 * mm)]
    cover = Table([
        [p("ผู้จัดทำ", "H2Thai"), p("นายปวริศช์ ประมวล")],
        [p("รหัสนักศึกษา", "H2Thai"), p("673380278-9")],
        [p("Section", "H2Thai"), p("1")],
        [p("รายวิชา", "H2Thai"), p("CP353002 Principles of Software Design")],
        [p("เทคโนโลยี", "H2Thai"), p("Spring Boot 3.3.0, Java 17, WebFlux, Reactor Netty, WebClient")],
    ], colWidths=[43 * mm, 112 * mm])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT), ("BOX", (0, 0), (-1, -1), 0.8, BLUE),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story += [cover, PageBreak()]

    story += [p("1. Reactive Programming และ Non-blocking I/O", "H1Thai"),
              p("Reactive Programming เป็นแนวทางประมวลผลข้อมูลในรูป stream แบบ asynchronous โดย publisher ส่งสัญญาณ onNext, onComplete หรือ onError ไปยัง subscriber การทำงานจึงประกอบ operator ต่อกันได้โดยไม่ต้องให้ thread รอผลลัพธ์ I/O"),
              p("Spring WebFlux เป็น reactive web stack ที่รองรับ Reactive Streams และทำงานแบบ non-blocking บน Reactor Netty ในโปรเจกต์นี้ controller คืน Mono/Flux ให้ framework เป็นผู้ subscribe และเขียน HTTP response"),
              p("Blocking เทียบกับ Reactive", "H2Thai")]
    compare = Table([
        [p("ประเด็น", "H2Thai"), p("Blocking", "H2Thai"), p("Reactive / Non-blocking", "H2Thai")],
        [p("การรอ I/O"), p("Thread รอจนงานเสร็จ"), p("คืน publisher แล้วใช้ callback/signal")],
        [p("รูปแบบข้อมูล"), p("คืนค่าโดยตรง"), p("คืน Mono หรือ Flux")],
        [p("การรองรับโหลด"), p("มักใช้หนึ่ง thread ต่อ request"), p("event-loop รองรับหลาย request ด้วย thread จำนวนน้อย")],
        [p("ตัวอย่าง client"), p("RestTemplate หรือ blocking call"), p("WebClient พร้อม operator chain")],
    ], colWidths=[35 * mm, 60 * mm, 75 * mm])
    compare.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [compare, Spacer(1, 7 * mm), p("Mono และ Flux", "H2Thai"),
              p("<b>Mono&lt;T&gt;</b> ส่งข้อมูลได้ 0 หรือ 1 ค่า เหมาะกับ findById, save, price และ Mono&lt;Void&gt; สำหรับ delete ส่วน <b>Flux&lt;T&gt;</b> ส่งข้อมูลได้ 0 ถึง N ค่า เหมาะกับ findAll และการค้นหาตาม category"),
              code('Mono<Product> one = repository.findById("1");\nFlux<Product> many = repository.findAll();')]

    story += [PageBreak(), p("2. สถาปัตยกรรมและ Operators", "H1Thai"),
              p("ระบบแยกหน้าที่ตาม Controller - Service - Repository เพื่อให้แต่ละชั้นมีความรับผิดชอบชัดเจน และใช้ constructor injection ตามหลัก Dependency Inversion"),
              code("HTTP Request\n    -> ProductController (Mono/Flux)\n    -> ProductService (business operators)\n    -> ProductRepository (ConcurrentHashMap)\n    -> Reactive signal -> HTTP Response"),
              p("Operators ที่ใช้", "H2Thai")]
    ops = Table([
        [p("Operator", "H2Thai"), p("ตำแหน่ง", "H2Thai"), p("หน้าที่", "H2Thai")],
        [p("map"), p("ProductService"), p("สร้าง ID และแปลง Product เป็น discountedPrice")],
        [p("filter"), p("ProductRepository"), p("กรองสินค้าที่ category ตรงกัน")],
        [p("flatMap"), p("ProductService / tests"), p("เชื่อม publisher สำหรับ save และ delete")],
        [p("switchIfEmpty"), p("ProductService"), p("เปลี่ยน empty publisher เป็น HTTP 404")],
        [p("defaultIfEmpty"), p("WebClient consumer"), p("กำหนดค่าทดแทนเมื่อ Mono ไม่มีข้อมูล")],
    ], colWidths=[32 * mm, 48 * mm, 90 * mm])
    ops.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [ops, Spacer(1, 6 * mm), p("WebClient method chain", "H2Thai"),
              p("get/post/delete เลือก HTTP method, uri กำหนด endpoint, retrieve เริ่มอ่าน response และ bodyToMono/bodyToFlux แปลง body เป็น reactive publisher จากนั้น caller chain operator ต่อได้ทันที"),
              code('productWebClient.getProductById("1")\n    .map(Product::getName)\n    .defaultIfEmpty("Product not found")\n    .subscribe(System.out::println);'),
              p("subscribe แสดงเฉพาะขอบระบบฝั่ง consumer ส่วน production controller/service ไม่ subscribe หรือ block เอง")]

    story += [PageBreak(), p("3. REST API ที่พัฒนา", "H1Thai")]
    endpoints = Table([
        [p("Method", "H2Thai"), p("Endpoint", "H2Thai"), p("Return", "H2Thai"), p("ผลลัพธ์", "H2Thai")],
        [p("GET"), p("/products"), p("Flux&lt;Product&gt;"), p("สินค้าทั้งหมด")],
        [p("GET"), p("/products/{id}"), p("Mono&lt;Product&gt;"), p("สินค้าตาม ID หรือ 404")],
        [p("POST"), p("/products"), p("Mono&lt;Product&gt;"), p("สร้างสินค้าและ UUID เมื่อไม่มี ID")],
        [p("DELETE"), p("/products/{id}"), p("Mono&lt;Void&gt;"), p("ลบสำเร็จคืน 204")],
        [p("GET"), p("/products/category/{category}"), p("Flux&lt;Product&gt;"), p("กรอง category")],
        [p("GET"), p("/products/{id}/price"), p("Mono&lt;Double&gt;"), p("ราคาหลังส่วนลด")],
    ], colWidths=[20 * mm, 64 * mm, 40 * mm, 46 * mm])
    endpoints.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [endpoints, Spacer(1, 7 * mm), p("กฎส่วนลด", "H2Thai"),
              p("NONE คืนราคาเดิม, MEMBER ลด 10% และ SEASONAL ลด 20% โดย Product.getDiscountedPrice() เป็นผู้คำนวณ")]

    evidence_pairs = [
        (("01-get-all-products.png", "ภาพที่ 1: GET /products - Flux<Product> คืนสินค้าตัวอย่าง"),
         ("02-get-product-by-id.png", "ภาพที่ 2: GET /products/1 - Mono<Product> พร้อมชื่อและรหัสนักศึกษา")),
        (("03-create-product.png", "ภาพที่ 3: POST /products - สร้างสินค้าและคืนข้อมูลที่บันทึก"),
         ("04-get-by-category.png", "ภาพที่ 4: GET /products/category/Accessories - filter ตาม category")),
        (("05-get-discounted-price.png", "ภาพที่ 5: GET /products/evidence-1/price - MEMBER 3500 ลดเหลือ 3150"),
         ("06-delete-product.png", "ภาพที่ 6: DELETE /products/evidence-1 - สำเร็จด้วย HTTP 204")),
    ]
    for index, pair in enumerate(evidence_pairs, start=4):
        story += [PageBreak(), p(f"{index}. หลักฐานการเรียก API จริง", "H1Thai")]
        story += evidence_image(*pair[0])
        story += evidence_image(*pair[1])

    story += [PageBreak(), p("7. โค้ด Reactive แต่ละชั้น", "H1Thai"),
              p("Repository", "H2Thai"),
              p("defer ทำให้การอ่านเกิดเมื่อมี subscriber, justOrEmpty รองรับกรณีไม่พบข้อมูล และ filter ใช้กับ Flux โดยไม่ต้องแปลงเป็น collection แบบ blocking"),
              code('public Mono<Product> findById(String id) {\n    return Mono.defer(() -> Mono.justOrEmpty(store.get(id)));\n}\n\npublic Flux<Product> findByCategory(String category) {\n    return findAll()\n        .filter(product -> category.equalsIgnoreCase(product.getCategory()));\n}'),
              p("Service", "H2Thai"),
              p("map จัดเตรียม ID, flatMap ส่งต่อไปยัง reactive repository และ switchIfEmpty คืน 404 เมื่อไม่พบสินค้า"),
              code('public Mono<Product> save(Product product) {\n    return Mono.just(product)\n        .map(item -> {\n            if (item.getId() == null || item.getId().isBlank())\n                item.setId(UUID.randomUUID().toString());\n            return item;\n        })\n        .flatMap(repository::save);\n}\n\npublic Mono<Double> getDiscountedPrice(String id) {\n    return getById(id).map(Product::getDiscountedPrice);\n}')]

    story += [PageBreak(), p("8. Controller และ WebClient", "H1Thai"),
              p("Controller", "H2Thai"),
              p("Controller คืน Mono/Flux โดยตรง Spring WebFlux จึงจัดการ subscription และ response lifecycle ให้ทั้งหมด"),
              code('@GetMapping\npublic Flux<Product> getAll() {\n    return service.getAll();\n}\n\n@PostMapping\npublic Mono<Product> save(@RequestBody Product product) {\n    return service.save(product);\n}\n\n@DeleteMapping("/{id}")\n@ResponseStatus(HttpStatus.NO_CONTENT)\npublic Mono<Void> delete(@PathVariable String id) {\n    return service.delete(id);\n}'),
              p("WebClient", "H2Thai"),
              p("WebClient ใช้ fluent API และ bodyToMono/bodyToFlux เพื่อคืน publisher ให้ caller ประกอบ operator ต่อ โดยไม่ใช้ block"),
              code('public Flux<Product> getAllProducts() {\n    return client.get()\n        .uri("/products")\n        .retrieve()\n        .bodyToFlux(Product.class);\n}\n\npublic Mono<Product> createProduct(Product product) {\n    return client.post()\n        .uri("/products")\n        .bodyValue(product)\n        .retrieve()\n        .bodyToMono(Product.class);\n}')]

    story += [PageBreak(), p("9. การทดสอบและผลลัพธ์", "H1Thai")]
    story += evidence_image("07-automated-tests.png", "ภาพที่ 7: ผล Maven tests จาก StepVerifier, WebTestClient และ WebClient integration")
    story += [p("ชุดทดสอบทั้งหมด 10 tests ผ่านโดยไม่มี failure หรือ error ครอบคลุม repository, service, ส่วนลดทั้งสามแบบ, HTTP endpoints และ ProductWebClient ที่เรียก Reactor Netty server จริงบน random port"),
              p("ตรวจ source แล้วไม่พบ .block(), blockFirst(), blockLast(), Thread.sleep() หรือ Future.get() ใน production code จึงไม่มีจุดที่ทำให้ endpoint รอผลแบบ blocking"),
              p("สรุป", "H2Thai"),
              p("ระบบสามารถสร้าง ดู ค้นหาตาม category คำนวณราคาหลังส่วนลด และลบสินค้าได้ด้วย Mono/Flux พร้อม WebClient ที่ chain operators ต่อได้ทันทีตามข้อกำหนด")]

    story += [PageBreak(), p("10. แหล่งอ้างอิง", "H1Thai"),
              p("1. Spring Framework Reference - Spring WebFlux<br/>https://docs.spring.io/spring-framework/reference/web/webflux.html"),
              p("2. Spring Framework Reference - WebClient<br/>https://docs.spring.io/spring-framework/reference/web/webflux-webclient.html"),
              p("3. Project Reactor Reference Guide - Getting Started<br/>https://projectreactor.io/docs/core/release/reference/gettingStarted.html"),
              p("4. Project Reactor API - Mono และ Flux<br/>https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html<br/>https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html"),
              Spacer(1, 12 * mm), p("Repository", "H2Thai"),
              p("https://github.com/PavaritPramual/posd-lab10-WebClient")]

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
