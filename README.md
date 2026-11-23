# CS:GO Raunt Sonucu Tahmini

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://csgoroundprediction-o4jxvrc4fx9azqit5kxn7j.streamlit.app)

Bu proje, CS:GO rekabetçi maç verileri üzerinden ekonomi farkı, harita-taraf dinamiği ve ardışık mağlubiyet serilerini kullanarak Logistic Regression ile raunt sonucunu tahmin eder.

## Canlı Web Uygulaması (Streamlit)

[![Streamlit Demo](images/demo.png)](https://csgoroundprediction-o4jxvrc4fx9azqit5kxn7j.streamlit.app)

## Proje Özeti ve Yaklaşım

- **Veri Temizleme:** Oyuncu ve hasar bazlı tekrar eden log satırları maç ve raunt (`file`, `round`) bazında tekilleştirildi.
- **Özellik Mühendisliği:**
  - `a_eq_diff`: 15. raunttan sonraki taraf değişimini (T ↔ CT) hesaba katarak Takım A'nın mevcut raunttaki ekipman değeri avantajı.
  - `map_side`: Harita ve oynanan taraf kombinasyonu (örn. `de_mirage_T`, `de_inferno_CT`).
  - `a_prev_streak` & `b_prev_streak`: Veri sızıntısını önlemek için mevcut raundun değil, bir önceki raundun ardışık mağlubiyet serisi (`shift(1)`).
- **Modelleme:** Eğitim ve test setleri ayrıldıktan sonra özellikler yalnızca eğitim seti istatistikleriyle (`StandardScaler`) ölçeklendi ve **Logistic Regression** modeli eğitildi.

## Model Performansı

| Model | Accuracy | ROC-AUC |
| :--- | :---: | :---: |
| Rastgele tahmin | %50.53 | - |
| Sadece ardışık mağlubiyet serisi | %64.37 | 0.6474 |
| Sadece ekipman farkı | %65.59 | 0.7161 |
| Tüm özellikler | %65.96 | 0.7191 |

Tahmin gücünün büyük kısmı ekipman farkından geliyor. Streak özellikleri tek başına da anlamlı bilgi taşıyor, ancak ekipman farkıyla yaklaşık ±0.54 korelasyonları olduğu için birlikte kullanıldıklarında ek katkıları küçük kalıyor (+0.37 puan accuracy).

## Görselleştirmeler

### 1. Ardışık Mağlubiyet Serisi ve Kazanma Oranı
![Streak Winrate](images/streak_winrate.png)

### 2. Model Katsayıları
![Feature Importance](images/feature_importance.png)

### 3. Model Değerlendirme (Confusion Matrix & ROC Eğrisi)
![Model Evaluation](images/model_evaluation.png)

## Kullanılan Teknolojiler
- **Python** (`pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `joblib`)
- **Streamlit** (Web Arayüzü ve Deployment)
- **Jupyter Notebook**

## Veri Seti
Bu çalışmada Kaggle üzerindeki [CS:GO Competitive Matchmaking Data](https://www.kaggle.com/datasets/skihikingkevin/csgo-matchmaking-damage) veri seti kullanılmıştır. Dosya boyutu nedeniyle ham veri repoya dahil edilmemiştir.
