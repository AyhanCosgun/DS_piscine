from pathlib import Path

# __file__, Python'un çalıştırılan dosyanın yolunu metin olarak tuttuğu özel değişkendir.
print(f"__file__: {__file__}")

# Path(__file__), bu metin yolunu pathlib.Path nesnesine dönüştürür.
# Böylece yol birleştirme ve klasör/dosya kontrolü gibi işlemler daha kolay yapılır.
print(f"Path(__file__): {Path(__file__)}")

# resolve(), yolu mutlak ve normalize edilmiş hale getirir; örneğin göreli parçaları
# çözer ve varsa sembolik bağlantıları gerçek hedeflerine kadar takip eder.
print(f"Path(__file__).resolve(): {Path(__file__).resolve()}")

# parent, dosyanın kendisini değil, dosyanın bulunduğu üst klasörü verir.
# Bu değer; çıktı dosyalarını aynı klasöre kaydetmek için kullanılabilir.
print(f"output_dir: {Path(__file__).resolve().parent}")
