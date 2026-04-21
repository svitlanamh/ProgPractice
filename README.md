# Проєкт BlockProcessor (Лабораторні 2-6)

Цей проєкт реалізує симулятор обробника подій блокчейну з використанням бази даних SQLite. Він демонструє еволюцію застосунку для обробки даних від базової роботи з CSV до інтеграції з базою даних, суворої валідації даних та автоматизованого тестування.

## 🗂️ Структура проєкту

Проєкт розділено на модульні компоненти, розроблені протягом кількох лабораторних робіт:

* **Лабораторна 2 (`lab2.py`, `lab2.csv`)**
    * Початкове налаштування та базові операції з обробки/парсингу даних.
* **Лабораторна 3 (`mydatabase.db`)**
    * Основна база даних SQLite, що містить таблиці для `BLOCKS`, `PERSONS`, `SOURCES`, `VOTES` та `event_stream`.
* **Лабораторна 4 (`lab4.py`, `models.py`)**
    * **`lab4.py`**: Класи в стилі об'єктно-реляційного відображення (ORM) для взаємодії з таблицями бази даних.
    * **`models.py`**: Інтеграція `pydantic` для забезпечення суворих правил валідації (наприклад, перевірка 8-символьних шістнадцяткових рядків для ідентифікаторів блоків та форматів IPv4).
* **Лабораторна 5 (`updater.py` / Логіка обробника блоків)**
    * Основний скрипт безперервного опитування. Він зчитує необроблені події з таблиці `event_stream`, обробляє події `vote` та `block`, обробляє конфлікти (такі як `DuplicateViewError` та `DuplicateBlockIdError`) і оновлює стан ланцюга в пам'яті.
* **Лабораторна 6 (`test_models.py`)**
    * Автоматизований набір тестів з використанням `pytest`, щоб переконатися, що всі моделі даних коректно приймають дійсні дані та відхиляють недійсні за допомогою перевірок Pydantic `ValidationError`.

---

## ⚙️ Архітектура системи та потік даних

Нижче наведено блок-схему Mermaid, яка ілюструє логіку циклу подій **BlockProcessor** при взаємодії з SQL бекендом. 

```mermaid
flowchart TD
    subgraph Database
        DB[(mydatabase.db)]
        ES[event_stream table]
        B[BLOCKS table]
    end

    subgraph BlockProcessor
        Poll[Poll for unprocessed events]
        Parse{Event Type?}
        
        ProcessVote[Add Vote to memory]
        FetchBlockView[Fetch block view from DB]
        
        PB[process_block function]
        Validate{Valid Block?}
        
        UpdateMem[Update in-memory chain, seen_ids, seen_views]
        Reject[Log Duplicate/Conflict Error]
        
        MarkProcessed[Mark event as is_processed = 1]
    end

    DB --- ES
    DB --- B

    ES -->|SELECT unprocessed| Poll
    Poll --> Parse

    Parse -->|vote| ProcessVote
    ProcessVote --> FetchBlockView
    
    Parse -->|block| FetchBlockView

    FetchBlockView -->|Create Block object| PB
    
    PB --> Validate
    Validate -->|No conflicts| UpdateMem
    Validate -->|ID/View exists| Reject

    UpdateMem --> MarkProcessed
    Reject --> MarkProcessed

    MarkProcessed -->|UPDATE query| ES
    
    style DB fill:#f9f,stroke:#333,stroke-width:2px
    style Poll fill:#bbf,stroke:#333,stroke-width:2px
    style Validate fill:#ffd,stroke:#333,stroke-width:2px
