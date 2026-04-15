# -*- coding: utf-8 -*-
"""Sınav verisi: data/*.json + assets/veriler.js (tek sayfa, fetch yok). Çalıştır: python3 scripts/build_exams.py"""
import json
import os
import random
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

# --- Doğru şık indeksi (0=A, 1=B, 2=C, 3=D) veri dosyalarında nasıl dağıtılsın? ---
# "rotate" — Sorular sırayla 0,1,2,3,0,1,... hedefe taşınır (yaklaşık eşit dağılım).
# "random" — Her soruda 0–3 arası rastgele hedef (RANDOM_SEED ile tekrarlanabilir).
# "none"   — EXAMS içindeki correct değeri ve şık sırası olduğu gibi yazılır.
CORRECT_INDEX_MODE = "rotate"
RANDOM_SEED = 42


def move_correct_answer_to_index(options, correct_idx, target_idx):
    """Doğru metni target_idx konumuna alır; şık listesi yeniden sıralanır."""
    opts = list(options)
    n = len(opts)
    if not (0 <= correct_idx < n) or not (0 <= target_idx < n):
        return opts, correct_idx
    label = opts.pop(correct_idx)
    opts.insert(target_idx, label)
    return opts, target_idx


def build_processed_exams():
    out = []
    rr = 0
    rnd = random.Random(RANDOM_SEED)
    for ex in EXAMS:
        qs = []
        for text, options, correct in ex["questions"]:
            opts, cor = list(options), correct
            if CORRECT_INDEX_MODE == "none":
                new_opts, new_cor = opts, cor
            elif CORRECT_INDEX_MODE == "rotate":
                target = rr % 4
                rr += 1
                new_opts, new_cor = move_correct_answer_to_index(opts, cor, target)
            elif CORRECT_INDEX_MODE == "random":
                new_opts, new_cor = move_correct_answer_to_index(opts, cor, rnd.randint(0, 3))
            else:
                raise ValueError("CORRECT_INDEX_MODE: none | rotate | random")
            qs.append({"text": text, "options": new_opts, "correct": new_cor})
        out.append({"title": ex["title"], "questions": qs})
    return out


# (soru metni, [A,B,C,D], doğru şık indeksi 0-3) — "none" dışı modlarda indeks üretimde yeniden hesaplanır
EXAMS = [
    {
        "title": "Acil durum, olay yeri ve 112",
        "questions": [
            (
                "Acilde başa çıkmada sıralamanın ilk basamağı genelde hangisidir?",
                [
                    "Hasta öyküsünü detaylı al",
                    "Olay yerini ve kişisel güvenliği değerlendir",
                    "Doğrudan kalp masajına başla",
                    "Önce hastayı araca bindir",
                ],
                1,
            ),
            (
                "Olay yerinde trafik kazasına müdahale ederken hangisi önceliklidir?",
                [
                    "İlk yardımcı reflektör ve trafik kurallarına dikkat etmelidir",
                    "Önce yaralıyı araçtan çek",
                    "Kaza yerini olduğu gibi bırak",
                    "Sadece telefonla kayıt al",
                ],
                0,
            ),
            (
                "Hasta/yaralıyı değerlendirmede ilk bakılması gerekenlerden biri hangisidir?",
                [
                    "Sadece tansiyon ölç",
                    "Bilinç, solunum ve belirgin kanama",
                    "Sadece nabız say",
                    "Yaralıyı ayakta yürüt",
                ],
                1,
            ),
            (
                "Türkiye'de acil yardım hattı numarası hangisidir?",
                ["155", "110", "112", "911"],
                2,
            ),
            (
                "Olay yeri güvenli değilken ilk yardımcı ne yapmalıdır?",
                [
                    "Risk alarak hemen yaklaş",
                    "Güvenliği sağlamadan veya sağlanmadan zorla müdahale et",
                    "Güvenliği artırıp riskleri azaltmaya çalış veya güvenli mesafede bekle",
                    "Olay yerini terk etmeden önce kimseyi bilgilendirme",
                ],
                2,
            ),
            (
                "İlk yardımın amaçlarından biri aşağıdakilerden hangisidir?",
                [
                    "Kesin tanı koymak",
                    "Yaşamı desteklemek ve durumu kötüleştirmemek",
                    "Hastanede yapılacak tedaviyi tek başına tamamlamak",
                    "İlacı reçetesiz vermek",
                ],
                1,
            ),
            (
                "Bilinç değerlendirmesinde ilk sorulabilecek basit ifade hangisidir?",
                [
                    "Nabzını sayalım mı?",
                    "İyi misiniz? / Kendinize geliyor musunuz?",
                    "Ailenizi arayayım mı?",
                    "Boynunuzu hareket ettirin",
                ],
                1,
            ),
            (
                "112 aramasında çağrı merkezine hangi bilgi özellikle önemlidir?",
                [
                    "Sadece yaralının adı",
                    "Olayın yeri, olayın türü ve hasta durumu özeti",
                    "İlk yardımcının mesleği",
                    "Hastanın TC kimlik numarası",
                ],
                1,
            ),
            (
                "İlk yardımcının kendini koruması neden önemlidir?",
                [
                    "Sadece yasal zorunluluk",
                    "İkinci bir kurban oluşmasını önlemek için",
                    "Daha hızlı koşabilmek için",
                    "Gereksizdir",
                ],
                1,
            ),
            (
                "Olay yerinde elektrik riski varsa yaklaşmadan önce ne düşünülmelidir?",
                [
                    "Önce su dök",
                    "Gücü kesme ve güvenli mesafe; gerekiyorsa uzaktan müdahale planı",
                    "Metal çubukla it",
                    "Eldiven yeterlidir, başka önlem gerekmez",
                ],
                1,
            ),
            (
                "Yaralıya yaklaşmadan önce çevrede hangi tehlike grupları değerlendirilmelidir?",
                [
                    "Sadece hava sıcaklığı",
                    "Kimyasal, yangın, trafik, elektrik vb. çevresel tehlikeler",
                    "Sadece yağmur",
                    "Sadece gürültü",
                ],
                1,
            ),
            (
                "İlk yardımda 'vücuda kontrol' (hızlı tarama) amacı nedir?",
                [
                    "Estetik değerlendirme",
                    "Yaşamı tehdit eden kanama ve solunum gibi bulguları fark etmek",
                    "Kırığı kesin tanılamak",
                    "Hastanın kilosunu tahmin etmek",
                ],
                1,
            ),
            (
                "Yaralıya müdahale sırasında hangisi doğru bir yaklaşımdır?",
                [
                    "Bildiğin her şeyi aynı anda yap",
                    "Öncelikleri belirleyip yaşamı tehdit edenlere önce müdahale et",
                    "Hareketi tamamen yasakla",
                    "Hastayı sürekli ayakta tut",
                ],
                1,
            ),
            (
                "İlk yardımcı olay yerinde koruyucu ekipman olarak ne kullanabilir?",
                [
                    "Sadece mendil",
                    "Eldiven, göz koruyucu gibi uygun bariyerler",
                    "Plastik poşet yeter",
                    "Koruyucu kullanmak yasaktır",
                ],
                1,
            ),
            (
                "Hasta bilinci kapalı görünüyorsa ilk genel yaklaşım hangisidir?",
                [
                    "Suya zorla içir",
                    "Hava yolunu ve solunumu değerlendirmek için temel kontroller",
                    "Boynunu çevirmeden sırtüstü bırakıp uzaklaş",
                    "Aspirin ver",
                ],
                1,
            ),
            (
                "Olay yerinde panik azaltmak için hangisi uygundur?",
                [
                    "Bağırmak",
                    "Sakin ve net talimatlar, gerekiyorsa yardım isteme",
                    "Kalabalığı yaralıya yığmak",
                    "Kimsenin 112 aramasına izin vermemek",
                ],
                1,
            ),
            (
                "İlk yardımda 'öykü' almak ne zaman değerlidir?",
                [
                    "Yaşam tehdidi giderilmeden önce uzun süreli sohbet",
                    "Güvenlik ve temel yaşam bulguları sonrası, uygun şekilde",
                    "Asla alınmaz",
                    "Sadece polis gelince",
                ],
                1,
            ),
            (
                "Yangın ortamında ilk yardımcı öncelikle ne yapmalıdır?",
                [
                    "Dumanın altından emniyetli çıkış ve güvenlik",
                    "Pencereden atla",
                    "Su bulunana kadar bekle",
                    "Asansörle in",
                ],
                0,
            ),
            (
                "Kazazedeyi taşımadan önce hangisi düşünülmelidir?",
                [
                    "Her zaman koşarak taşı",
                    "Omurga yaralanması riski ve uygun taşıma tekniği",
                    "Taşıma yasaktır",
                    "Sadece kucakta taşı",
                ],
                1,
            ),
            (
                "İlk yardım eğitiminde vurgulanan temel ilke hangisidir?",
                [
                    "Zarar verme (zararı artırmama)",
                    "Hızlı taburcu",
                    "Tanı koyma zorunluluğu",
                    "İlacı mutlaka ver",
                ],
                0,
            ),
        ],
    },
    {
        "title": "TYD: temel yaşam desteği",
        "questions": [
            (
                "TYD sırasında solunumu kontrol etmek için önerilen süre üst sınırı yaklaşık kaç saniyedir?",
                ["3 saniye", "5 saniye", "10 saniyeyi geçmemeli", "30 saniye"],
                2,
            ),
            (
                "Yetişkinde temel yaşam desteğinde tek kurtarıcıya göre göğüs basısı / suni solunum oranı genelde hangisidir?",
                ["15:2", "30:2", "5:1", "50:2"],
                1,
            ),
            (
                "TYD'ye başlamadan önce bilinç kontrolünde sık kullanılan yaklaşım hangisidir?",
                [
                    "Omuzdan hafifçe sarsarak ve seslenerek yanıt alma",
                    "Gözüne su sık",
                    "Ayak bileğinden çek",
                    "Parmak ucuyla batırarak uyandırma",
                ],
                0,
            ),
            (
                "Hava yolu açıklığı için sık öğretilen baş-çene manevrası hangi amaçla yapılır?",
                [
                    "Boynu kırmak",
                    "Dil ve yumuşak damağın geriye kaymasını azaltarak hava yolunu açmak",
                    "Kusmayı önlemek",
                    "Nabız artırmak",
                ],
                1,
            ),
            (
                "Yetişkinde göğüs kompresyonu için el yerleşimi nereye önerilir?",
                [
                    "Karnın ortası",
                    "Göğüs kemiğinin alt yarısı / orta hat (kompresyon bölgesi)",
                    "Sol köprücük kemiği üstü",
                    "Boynun yan tarafı",
                ],
                1,
            ),
            (
                "Yetişkinde önerilen kompresyon hızı dakikada yaklaşık kaç basıdır?",
                ["60-80", "80-99", "100-120", "140-160"],
                2,
            ),
            (
                "Yetişkinde önerilen kompresyon derinliği yaklaşık olarak hangi aralıktadır?",
                ["1-2 cm", "3-4 cm", "5-6 cm", "8-10 cm"],
                2,
            ),
            (
                "Çocukta (kompresyon uygulanan grup) derinlik yaklaşık olarak kaç cm olarak öğretilir?",
                ["2 cm", "3 cm", "5 cm", "8 cm"],
                2,
            ),
            (
                "Bebekte göğüs kompresyon derinliği yaklaşık kaç cm olarak öğretilir?",
                ["1 cm", "2 cm", "4 cm", "7 cm"],
                2,
            ),
            (
                "Kompresyon derinliği genel olarak göğüs ön-arka çapının yaklaşık kaçı olarak ifade edilir?",
                ["1/10", "1/6", "1/3", "Tamamı"],
                2,
            ),
            (
                "TYD ne zamana kadar sürdürülmelidir?",
                [
                    "2 dakika sonra kesin dur",
                    "Solunum dönene, profesyonel yardım gelene veya ilk yardımcı tükenene kadar",
                    "Sadece 112 arandıysa",
                    "30 bası sonra",
                ],
                1,
            ),
            (
                "TYD sırasında her kaç döngüde bir kısa yeniden değerlendirme önerilir?",
                ["1 döngü", "3 döngü", "5 döngü", "10 döngü"],
                2,
            ),
            (
                "İki kurtarıcı bulunduğunda çocuk ve bebekte bası:solunum oranı genelde nasıl öğretilir?",
                ["30:2", "15:2", "50:2", "5:1"],
                1,
            ),
            (
                "Solunumu olmayan yetişkinde ilk temel adımlardan biri hangisidir?",
                [
                    "Sadece beklemek",
                    "112'yi aramak / yardım istemek ve TYD'ye başlamak",
                    "Su içirmek",
                    "Aspirin vermek",
                ],
                1,
            ),
            (
                "TYD öncesi olay yeri güvenliği ile ilgili doğru ifade hangisidir?",
                [
                    "TYD'de güvenlik önemli değildir",
                    "Önce sahayı güvenli hale getirmeye çalışmak önemlidir",
                    "Sadece hastaya odaklan",
                    "Her zaman araç içinde yap",
                ],
                1,
            ),
            (
                "OED (AED) kullanımı TYD ile ilişkisi açısından nasıl düşünülmelidir?",
                [
                    "OED gelene kadar TYD yapılmaz",
                    "Mümkün olan en kısa sürede getirip talimatlara uyarak kullanmak",
                    "Sadece doktor gelince",
                    "Sadece hastanede",
                ],
                1,
            ),
            (
                "Suni solunum yapılabiliyorsa her bir solunum yaklaşık ne kadar sürmelidir?",
                ["3 saniye üstü", "1 saniyeden kısa", "Yaklaşık 1 saniye", "10 saniye"],
                2,
            ),
            (
                "Göğüs kompresyonu sırasında göğüsün tamamen sıkışması (rebound) için ne önemlidir?",
                [
                    "Basıştan sonra göğsün yeniden genişlemesine izin vermek",
                    "Göğse sürekli basılı tutmak",
                    "Hızı düşürmekten kaçınmak için rebound yapmamak",
                    "Sadece dirsek kilidi",
                ],
                0,
            ),
            (
                "Bilinç kapalı ama düzenli solunumu olan hastada genel yaklaşım hangisidir?",
                [
                    "TYD'ye hemen başla",
                    "Hava yolunu koruyup yan yatış (iyileşme pozisyonu) düşün",
                    "Ayakta yürüt",
                    "Sırtüstü yastıksız bırak",
                ],
                1,
            ),
            (
                "Beynin oksijensiz kalabileceği kritik süre eğitimlerde genelde kaç dakika bandında anlatılır?",
                ["1-2 dakika", "4-6 dakika", "30 dakika", "2 saat"],
                1,
            ),
        ],
    },
    {
        "title": "OED ve yaşam zinciri",
        "questions": [
            (
                "OED (otomatik eksternal defibrilatör) temel amacı nedir?",
                [
                    "Kan basıncını ölçmek",
                    "Uygun vakalarda şok ile yaşamı tehdit eden ritimleri düzeltmeye yardımcı olmak",
                    "İlaç enjekte etmek",
                    "Röntgen çekmek",
                ],
                1,
            ),
            (
                "OED kullanımında cihazın sesli/t yazılı uyarılarına uyulması neden önemlidir?",
                [
                    "Ritim analizi ve şok güvenliği için",
                    "Sadece pil tasarrufu",
                    "Zorunlu değil",
                    "Sadece kayıt için",
                ],
                0,
            ),
            (
                "OED kullanımında ıslak zemin veya metal yüzey yakınında dikkat edilmesinin nedeni nedir?",
                [
                    "Sadece hijyen",
                    "Elektriksel güvenlik ve doğru enerji iletimi riskleri",
                    "Cihaz garantisi",
                    "Gürültü",
                ],
                1,
            ),
            (
                "Yenidoğanda (0-28 gün) OED kullanımı ile ilgili genel yaklaşım hangisidir?",
                [
                    "Asla kullanılmaz",
                    "Gerekirse kullanılabilir; mümkünse pediatrik ped/ped mod tercih edilir",
                    "Her zaman yetişkin ped kullan",
                    "Sadece evde",
                ],
                1,
            ),
            (
                "Kalıcı pacemaker olan hastada OED kullanımı genel olarak nasıl değerlendirilir?",
                [
                    "Kesinlikle yasak",
                    "Pedleri uygun konuma yerleştirip kullanılabilir (klinik protokollere uygun)",
                    "Sadece pil değişiminden sonra",
                    "Sadece çocuklarda",
                ],
                1,
            ),
            (
                "Gebelikte OED kullanımı ile ilgili genel bilgi hangisidir?",
                [
                    "Gebelikte asla kullanılmaz",
                    "Anne yaşamını korumak için gerekirse kullanılabilir",
                    "Sadece sezaryen sonrası",
                    "Sadece ilk trimesterde",
                ],
                1,
            ),
            (
                "Yaşam zincirinin (chain of survival) halkalarından biri aşağıdakilerden hangisidir?",
                [
                    "Hastane faturası",
                    "Erken tanı / yardım çağrısı ve erken TYD",
                    "Sosyal medya paylaşımı",
                    "Eczane stoğu",
                ],
                1,
            ),
            (
                "Yaşam zincirinde 'erken defibrilasyon' ne anlama gelir?",
                [
                    "İlk yardımcının erken eve dönmesi",
                    "OED ile mümkün olan en kısa sürede ritim düzeltme şansı",
                    "Sadece ilaç",
                    "Sadece ameliyat",
                ],
                1,
            ),
            (
                "OED pedlerinin yerleştirilmesinde yaygın öneri hangisidir?",
                [
                    "İkisini de karına",
                    "Birini sağ üst göğüs altına, diğerini sol koltuk altına (ön-arka alternatifleri cihaza göre)",
                    "Boynun iki yanına",
                    "Bacak bileklerine",
                ],
                1,
            ),
            (
                "Şok öncesi herkesin hastadan uzaklaştırılması neden istenir?",
                [
                    "Fotoğraf çekmek için",
                    "Şok enerjisinin yanlışlıkla başkasına geçmemesi için",
                    "Gürültü",
                    "Zorunlu değil",
                ],
                1,
            ),
            (
                "OED 'şok önermiyor' dediğinde genelde ne yapılır?",
                [
                    "TYD'ye devam ve talimatları izle",
                    "Cihazı kapatıp git",
                    "Hastayı taşı",
                    "Su dök",
                ],
                0,
            ),
            (
                "İleri yaşam desteği ve sonrası bakım yaşam zincirinde nereye oturur?",
                [
                    "Sadece evde bakım",
                    "Hastane içi ileri tedavi ve iyileşme süreçleri",
                    "İlk yardımcı sertifikası",
                    "Sadece eczane",
                ],
                1,
            ),
            (
                "OED getirilirken kurtarıcı ne yapmalıdır?",
                [
                    "TYD'yi kesintisiz sürdürmeye çalışmak",
                    "TYD'yi durdurmak",
                    "Sadece beklemek",
                    "Hastayı oturtmak",
                ],
                0,
            ),
            (
                "OED kullanımında metal takı/toka gibi unsurlar için genel öneri nedir?",
                [
                    "Hiç önemli değil",
                    "Mümkünse ped altına gelmeyecek şekilde çıkar/uzaklaştır",
                    "Daha iyi iletim için artır",
                    "Sadece altın için",
                ],
                1,
            ),
            (
                "Ventriküler fibrilasyon gibi ritimlerde erken defibrilasyonun önemi nedir?",
                [
                    "Gecikmenin başarı şansını düşürmesi",
                    "Hiçbir etkisi yok",
                    "Sadece nabız sayımını kolaylaştırması",
                    "Sadece ağrı kesmesi",
                ],
                0,
            ),
            (
                "TYD + OED yaklaşımında öncelik hangi sıraya yakındır?",
                [
                    "Önce uzun süre bekleyip sonra TYD",
                    "Erken çağrı, erken TYD, erken OED",
                    "Sadece OED",
                    "Sadece suni solunum",
                ],
                1,
            ),
            (
                "OED analiz sırasında hastaya dokunulmamasının nedeni nedir?",
                [
                    "Ritim analizinin bozulmaması",
                    "Cihazın kapanması",
                    "Hastanın uyanması",
                    "Trafik",
                ],
                0,
            ),
            (
                "Solunum geri gelirse ve hasta stabil ise hangi pozisyon akla gelir?",
                ["Sırtüstü düz", "Yan yatış (iyileşme pozisyonu)", "Oturuş", "Yüzüstü"],
                1,
            ),
            (
                "İlk yardımcı yorulduğunda ne yapılmalıdır?",
                [
                    "TYD kesinlikle durdurulmaz, mümkünse yer değiştirme / devretme",
                    "Her zaman tek başına devam",
                    "Sadece su iç",
                    "Hastayı bırak",
                ],
                0,
            ),
            (
                "Resmî ilk yardım eğitim sunumlarına ulaşmak için hangi kurum sayfası kullanılabilir?",
                [
                    "Sadece sosyal medya",
                    "Sağlık Bakanlığı acil sağlık / ilk yardım sunumları sayfası",
                    "Sadece yabancı siteler",
                    "Sadece forum",
                ],
                1,
            ),
        ],
    },
    {
        "title": "Bilinç, inme (FAST) ve pozisyon",
        "questions": [
            (
                "USAY bilinç düzeyi sıralamasında 'U' neyi ifade eder?",
                ["Yanıtsız", "Uyanık (alert)", "Ağrıya yanıt", "Sese yanıt"],
                1,
            ),
            (
                "USAY'da 'S' hangi düzeyle ilişkilendirilir?",
                ["Uyanık", "Sese yanıt", "Ağrıya yanıt", "Yanıtsız"],
                1,
            ),
            (
                "USAY'da 'A' hangi düzeyle ilişkilendirilir?",
                ["Uyanık", "Sese yanıt", "Ağrıya yanıt", "Yanıtsız"],
                2,
            ),
            (
                "USAY'da 'Y' ne anlama gelir?",
                ["Yaralı", "Yanıtsız", "Yürüyebilir", "Yüksek ateş"],
                1,
            ),
            (
                "FAST inme tanımsal kontrolünde 'F' neyi hatırlatır?",
                ["Foot bacak", "Face yüz asimetrisi/kayma", "Fever ateş", "Food yemek"],
                1,
            ),
            (
                "FAST'ta 'A' neyi kontrol etmeyi hatırlatır?",
                ["Ağrı", "Arm kol güçsüzlüğü/düşmesi", "Ateş", "Ayak şişliği"],
                1,
            ),
            (
                "FAST'ta 'S' neyi kontrol etmeyi hatırlatır?",
                ["Solunum sayısı", "Speak konuşma bozukluğu", "Şok", "Serum"],
                1,
            ),
            (
                "Bazı eğitimlerde FAST'ın son harfi zaman/112 araması veya güvenli nakil ile ilişkilendirilir. Hangisi uygundur?",
                [
                    "Durumu fark edince gecikmeden 112'yi aramak",
                    "Sadece evde beklemek",
                    "Sadece sosyal medyada paylaşmak",
                    "Hastayı koşturarak yormak",
                ],
                0,
            ),
            (
                "İnme şüphesinde ilk yardımcının önceliği genelde nedir?",
                [
                    "Aspirin vermek",
                    "Zaman kaybetmeden 112 ve hastane değerlendirmesi",
                    "Masaj yağı sürmek",
                    "Bol su içirmek",
                ],
                1,
            ),
            (
                "Bilinç kapalı ama solunumu olan hastada hava yolunu korumak için hangi pozisyon düşünülür?",
                ["Yüzüstü", "Sırtüstü baş geri", "Yan yatış (iyileşme pozisyonu)", "Oturur"],
                2,
            ),
            (
                "Yan yatışta genel amaçlardan biri nedir?",
                [
                    "Kusmayı kolaylaştırıp hava yolunu açık tutmaya yardım",
                    "Bel ağrısını kesin tedavi",
                    "Kırığı düzelt",
                    "Nabız artır",
                ],
                0,
            ),
            (
                "Omurga travması şüphesi varsa yan yatış ile ilgili dikkat edilmesi gereken nedir?",
                [
                    "Her zaman zorla yan çevir",
                    "Stabilizasyon ve şüphe varsa hareketi minimize etme yaklaşımı",
                    "Sadece ayakta tut",
                    "Omurgayı bükerek çevir",
                ],
                1,
            ),
            (
                "Bilinç bozukluğunda ilk değerlendirmede solunum kontrolü için üst süre yaklaşık kaç saniyedir?",
                ["30 saniye", "10 saniyeyi geçmemeli", "60 saniye", "2 dakika"],
                1,
            ),
            (
                "Hasta sese yanıt veriyor ama tam uyanık değilse USAY'da yaklaşık hangi düzey düşünülür?",
                ["Uyanık", "Sese yanıt", "Yanıtsız", "Ağrıya yanıt"],
                1,
            ),
            (
                "Konuşma bozukluğu ve yüz kayması birlikte görülürse hangi acil düşünülmelidir?",
                ["Basit migren", "İnme veya benzeri nörolojik acil", "Sadece yorgunluk", "Alerji"],
                1,
            ),
            (
                "Bilinçli hastada göğüs ağrısı ve nefes darlığı varsa ilk yaklaşım hangisidir?",
                [
                    "Stresten kesinlikle kaynaklanır, bekle",
                    "112 ve acil değerlendirme",
                    "Ağır egzersiz yaptır",
                    "Sıcak duş",
                ],
                1,
            ),
            (
                "Hipoglisemi şüphesinde bilinçli ve yutabilen hastada ne düşünülebilir?",
                [
                    "Şekerli içecek/yiyecek (protokole uygun)",
                    "Sadece su",
                    "Alkol",
                    "Aç bırak",
                ],
                0,
            ),
            (
                "Nöbet sonrası hasta yarı bilinçli ve solunumu iyi ise genel yaklaşım?",
                [
                    "Zorla ağızdan yemek ver",
                    "Güvenli yan yatış ve 112 değerlendirmesi",
                    "Sırtüstü baş geri zorla",
                    "Koştur",
                ],
                1,
            ),
            (
                "Bilinç değerlendirmesinde 'ağrıya yanıt' nasıl test edilebilir?",
                [
                    "Kırık bölgeye şiddetli vurma",
                    "Trapezius sıkma gibi uyaranlarla yanıt arama (eğitimde öğretilen uygun uyaran)",
                    "Gözüne dokunma",
                    "Test etme yasak",
                ],
                1,
            ),
            (
                "İlk yardımcı bilinç düzeyini kaydederken ne fayda sağlar?",
                [
                    "112 ve sağlık ekibine iletilen net bilgi",
                    "Sadece merak",
                    "Hastayı utandırmak",
                    "Yasak",
                ],
                0,
            ),
        ],
    },
    {
        "title": "Kanama, şok ve yaralanma özeti",
        "questions": [
            (
                "Yaşamı tehdit eden dış kanamada ilk yaklaşım hangisidir?",
                [
                    "Kanamayı görmeyi reddet",
                    "Doğrudan ve güçlü bası ile basınç uygulama",
                    "Yarayı sıcak suyla yıka",
                    "Yarayı açık bırak",
                ],
                1,
            ),
            (
                "Uzuv kopması gibi ciddi kanamalarda turnike düşünülürken dikkat edilmesi gereken nedir?",
                [
                    "Hiç kullanılmaz",
                    "Yaşamı tehdit eden kanamada uygun şekilde ve mümkünse eğitimle",
                    "Her küçük keside",
                    "Sadece baş parmak için",
                ],
                1,
            ),
            (
                "Şok bulgularından biri aşağıdakilerden hangisi olabilir?",
                [
                    "Ciltte solukluk/soğuk terleme, hızlı nabız",
                    "Sadece yüksek ateş",
                    "Sadece kaşıntı",
                    "Sadece hapşırık",
                ],
                0,
            ),
            (
                "Şokta hasta yatırılırken hangi pozisyon genelde öğretilir (omurga travması yoksa)?",
                [
                    "Ayakları yükseltilmiş şok pozisyonu düşünülebilir",
                    "Baş aşağı dik",
                    "Oturur ve eğilmez",
                    "Yüzüstü",
                ],
                0,
            ),
            (
                "Göğüs ağrısı ve şok tablosu birlikte görülürse öncelik?",
                ["Evde çay", "112 ve acil yardım", "Masaj", "Uyku"],
                1,
            ),
            (
                "Burun kanamasında genel öneri hangisidir?",
                [
                    "Başı geri eğ",
                    "Burnu sıkıp 10-15 dk kadar öne eğilmiş başla basınç",
                    "Burun içine pamuk zorla it",
                    "Sıcak kompres göğse",
                ],
                1,
            ),
            (
                "Yabancı cisim solunum yolunda tam tıkanıklıkta bilinçli yetişkinde hangi manevra öğretilir?",
                ["Heimlich / abdominal thrust", "Sırtüstü baş geri", "Su içir", "Kusturucu ilaç"],
                0,
            ),
            (
                "Hamile veya obez hastada tıkanıklıkta alternatif olarak ne öğretilir?",
                [
                    "Karın thrust",
                    "Göğüs thrust",
                    "Sadece beklemek",
                    "Zıplatmak",
                ],
                1,
            ),
            (
                "Bilinçli çocukta tıkanıklıkta pozisyon genelde nasıldır?",
                ["Ayakta veya oturur, yaş grubuna uygun thrust", "Ters asarak", "Yüzüstü yastıksız", "Koşarak"],
                0,
            ),
            (
                "Hayvan ısırığında ilk yaklaşım hangisidir?",
                [
                    "Yarayı yıkayıp kanamayı kontrol edip 112/yaralı bakımına yönlendirme",
                    "Isıran hayvanı yakalamaya zorla",
                    "Yarayı kapatma yok",
                    "Alkol dök",
                ],
                0,
            ),
            (
                "Zehirlenmede bilinçli hastaya genel olarak ne yapılmamalıdır?",
                [
                    "Kusturmaya zorlamak ve bilinçsiz hastaya ağızdan içecek vermek",
                    "112 aramak",
                    "Örnekleri not etmek",
                    "Konteyneri göstermek",
                ],
                0,
            ),
            (
                "Yanıkta ilk soğutma ile ilgili genel öneri hangisidir?",
                [
                    "Buz doğrudan uzun süre",
                    "Ilık akan su ile sınırlı süre soğutma (eğitimde öğretilen)",
                    "Yağ sür",
                    "Patlat",
                ],
                1,
            ),
            (
                "Kırık şüphesinde genel ilke hangisidir?",
                [
                    "Hareket ettirerek test et",
                    "İmmobilizasyon ve ağrıyı artırmadan stabilize etme",
                    "Masajla düzelt",
                    "Sıcak kompres",
                ],
                1,
            ),
            (
                "Açık göğüs yaralanmasında riskli durum hangisidir?",
                [
                    "Pnömotoraks / hava embolisi riski",
                    "Sadece kaşıntı",
                    "Sadece morluk",
                    "Hiç risk yok",
                ],
                0,
            ),
            (
                "Göz yanığında ilk yaklaşım hangisidir?",
                [
                    "Ovuştur",
                    "Bol temiz su ile yıkama ve 112",
                    "Merhem sık",
                    "Gözü kapatıp bekle",
                ],
                1,
            ),
            (
                "Boğulma (suda) bilinci kapalı çıkarılan hastada öncelik?",
                [
                    "Sadece battaniye",
                    "Hava yolu ve solunum/TYD ve 112",
                    "Ayakta yürüt",
                    "Yemek ver",
                ],
                1,
            ),
            (
                "Arı/böcek sokmasında ağır alerji şüphesinde?",
                [
                    "Bekle ve gözlemle",
                    "112 ve acil değerlendirme (epinefrin vb. sağlıkçı kararı)",
                    "Sıcak su",
                    "Limon sık",
                ],
                1,
            ),
            (
                "Kan şeker düşüklüğünde bilinç kapalı hastaya ağızdan şeker vermek?",
                [
                    "Tehlikeli aspirasyon riski; yasak",
                    "Her zaman verilir",
                    "Sadece sıcak çikolata",
                    "Sadece meyve suyu zorla",
                ],
                0,
            ),
            (
                "Yaralı taşırken omurga korunması neden önemlidir?",
                [
                    "Sinir hasarını kötüleştirmemek",
                    "Daha hızlı koşmak",
                    "Estetik",
                    "Gerekmez",
                ],
                0,
            ),
            (
                "İlk yardımda enfeksiyon kontrolü için hangisi önerilir?",
                [
                    "Yaraya üflemek",
                    "Temiz malzeme, mümkünse eldiven ve yara örtüsü",
                    "Kirli bez",
                    "Tükürük",
                ],
                1,
            ),
        ],
    },
]

assert len(EXAMS) == 5
for ex in EXAMS:
    assert len(ex["questions"]) == 20

PROCESSED = build_processed_exams()

catalog = {
    "exams": [
        {"id": str(i + 1), "title": PROCESSED[i]["title"], "file": f"exam-{i+1}.json"}
        for i in range(5)
    ]
}

for i, ex in enumerate(PROCESSED, start=1):
    payload = {"title": ex["title"], "questions": ex["questions"]}
    path = os.path.join(DATA, f"exam-{i}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

with open(os.path.join(DATA, "exams.json"), "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

ASSETS = os.path.join(ROOT, "assets")
embedded = []
for i, ex in enumerate(PROCESSED, start=1):
    embedded.append({"id": str(i), "title": ex["title"], "questions": ex["questions"]})
veriler_path = os.path.join(ASSETS, "veriler.js")
with open(veriler_path, "w", encoding="utf-8") as f:
    f.write("// Gömülü sınav listesi — düzenle veya bu script ile yeniden üret\n")
    f.write("window.ILKYARDIM_EXAMS = ")
    json.dump(embedded, f, ensure_ascii=False, indent=2)
    f.write(";\n")

_dist = Counter()
for _ex in PROCESSED:
    for _q in _ex["questions"]:
        _dist[_q["correct"]] += 1
print("Wrote exam-1..5.json, exams.json and assets/veriler.js")
print("  CORRECT_INDEX_MODE=%r -> doğru indeks dağılımı (0=A..3=D): %s" % (CORRECT_INDEX_MODE, dict(sorted(_dist.items()))))
