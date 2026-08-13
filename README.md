#  Measurement Data Scheduler & Experiment Management System

Bu proje, yüksek hacimli ölçüm verilerinin işlenmesi, öncelikli görevlerin zamanlanması (task scheduling), hızlı arama ve veri tutarlılığının (atomik çalışma) sağlanması amacıyla geliştirilmiş bir veri yönetim sistemidir.

---

##  Sistem Mimarisi ve Tasarım Kararları

Sistemin merkezinde, tüm alt modülleri orkestre eden **`ExperimentManager`** bulunmaktadır. `ExperimentManager`, bağımlılıkları kendi içinde üretmek yerine **Dependency Injection (DI)** prensibiyle dışarıdan alır ve **Composition** ilişkisi kurar.

```text
                    +-----------------------+
                    |   ExperimentManager   |
                    +-----------------------+
                                |
        +-----------------------+-----------------------+
        | (DI)                  | (DI)                  | (DI)
        v                       v                       v
+---------------+       +---------------+       +---------------+
|  Repository   |       |    Buffer     |       |   Scheduler   |
| (Dict Index)  |       |    (Deque)    |       | (PriorityHeap)|
+---------------+       +---------------+       +---------------+