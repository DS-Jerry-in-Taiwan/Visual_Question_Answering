下面是「補 1–2 條變化查詢」後，更新過的 Phase 2‑A 情境模板，以及一份可直接放進 repo 的 `standard_queries.md`（完整第一版，聚焦在暴力／打架事件情境）。

***

## 更新後的 Phase 2‑A 情境說明（暴力／打架事件）

**情境名稱：**  
事後調查：在指定時段與區域內，查詢是否發生暴力／打架事件

**任務邊界：**

- 本階段關注的事件型態：
  - 肢體衝突、打架、追逐攻擊、多人爭執演變成推擠／毆打。
- 查詢條件特性：
  - 以自然語言描述 + 可選的時間區間與大致地點（停車場、大門口、樓層走廊）。
- 不要求／不涵蓋：
  - 精準法律分類（傷害 vs 口角 vs 推擠），只要畫面中明顯有衝突即可視為候選。
  - 人物身分識別與跨攝影機長時間追蹤。
  - 需要整合多支攝影機序列才能判斷的複雜案情。

***

## standard_queries.md（可直接放進 repo）

```markdown
# Phase 2 標準查詢集（standard_queries.md）

本文件定義 Phase 2 的「暴力／打架事件事後調查」情境下的標準查詢集，作為：
- 任務邊界的具體化說明；
- 後續檢索品質評估（Recall@K / Precision@K）與體驗調整的固定基準集合。

---

## 1. 任務邊界（Phase 2‑A Scope）

### 1.1 本情境聚焦的查詢意圖類別

本階段聚焦於單一主情境：

- **暴力／打架事件（physical_fight）**

說明：

- 關注是否在特定區域、特定時段發生明顯肢體衝突／打架事件。
- 期望透過查詢快速找到代表性的事件片段（含時間與地點），作為事後調查線索。

### 1.2 暫不涵蓋的場景

以下類型暫不作為 Phase 2 的正式目標：

- 精準人物身分辨識與跨攝影機追蹤同一個人；
- 僅有言語爭吵但沒有明顯肢體衝突的情況；
- 需要結合多支攝影機長時間序列才能判斷的複雜案件。

---

## 2. 查詢條目結構（模板）

每條標準查詢使用以下欄位：

- `query_id`：唯一 ID（大寫 + 下劃線）
- `intent`：意圖類別（本情境統一使用 `physical_fight`）
- `text`：實際使用的自然語言查詢句
- `business_description`：這條查詢在安防業務上的目的與背景
- `scope_notes`：邊界說明（接受哪些誤差、不要求什麼）
- `required_metadata`：執行與呈現這條查詢所需的重要欄位（timestamp、camera_id 等）
- `example_expected_results`：1–2 個理想命中的事件輪廓描述（非必須與實際資料完全對應，用於對齊預期）

---

## 3. 標準查詢集：暴力／打架事件（physical_fight）

> 提示：以下為第一版標準查詢集，之後可視實際安防場域與資料分佈增修。

```
- query_id: VIOLENCE_PARKING_NIGHT_01
  intent: physical_fight
  text: "昨晚停車場裡有沒有發生打架或明顯的肢體衝突？"
  business_description: >
    事後接獲投訴或警方詢問時，用來快速確認停車場是否有明顯的打架場面，
    並找出對應的影像片段作為佐證或進一步調查依據。
  scope_notes: >
    不要求精準區分「推擠」或「毆打」，只要畫面上出現多人的激烈肢體互動、
    追打、推倒等，都視為候選結果。
    若時間與使用者口語指定的「昨晚」大致相符（例如 18:00–06:00 區間內），視為可接受。
  required_metadata:
    - timestamp
    - camera_id
    - location
  example_expected_results:
    - "停車場中段，一群人圍在一起揮拳推擠，持續約數十秒"
    - "兩人在車旁發生激烈爭執並互相推撞"

- query_id: VIOLENCE_ENTRANCE_NIGHT_01
  intent: physical_fight
  text: "昨天深夜在大門口有沒有發生任何打架或暴力衝突？"
  business_description: >
    用於回顧大門出入口是否發生明顯衝突事件，
    例如客戶與保全、訪客與訪客之間的肢體衝突。
  scope_notes: >
    只關注大門攝影機所涵蓋的區域，不跨其他攝影機。
    若只是非常短暫的肢體接觸（例如一兩秒的推擠），可視情況標註為弱相關。
  required_metadata:
    - timestamp
    - camera_id
    - location
  example_expected_results:
    - "大門外兩人在門口前互相揮拳，保全介入勸阻並分開雙方"

- query_id: VIOLENCE_CORRIDOR_EVENING_01
  intent: physical_fight
  text: "今天傍晚在三樓走廊是否有學生之間的打架或肢體衝突？"
  business_description: >
    用於校園或辦公樓情境，事後確認特定樓層走廊是否發生打架事件，
    協助導師、管理員或安管單位調查通報內容。
  scope_notes: >
    聚焦在指定樓層與走廊區域，不需跨樓層比對。
    若只是短暫追逐但未有明顯肢體接觸，可視為次要結果或不列入主要命中。
  required_metadata:
    - timestamp
    - camera_id
    - location
    - floor
  example_expected_results:
    - "三樓走廊，兩名學生在教室外互相推擠並短暫揮拳"
    - "三樓樓梯口附近，有多名學生圍觀兩人衝突"

- query_id: VIOLENCE_BACK_ALLEY_NIGHT_01
  intent: physical_fight
  text: "昨晚後巷或建築物側邊小路有沒有出現打架或暴力事件？"
  business_description: >
    用於檢查較隱蔽區域（如後巷、建築物側邊小路）是否發生衝突事件，
    這類區域常是正式出入口監控不到、但實際風險較高的地方。
  scope_notes: >
    允許系統從覆蓋這些陰暗角落或後巷的攝影機中找出疑似衝突畫面。
    不要求具體辨識參與人數，只需能標出有明顯肢體衝突的片段。
  required_metadata:
    - timestamp
    - camera_id
    - location
  example_expected_results:
    - "建築物後方巷子中兩人在牆邊扭打，畫面光線較暗但動作明顯"
```

---

## 4. 說明：為什麼這樣就可以視為 Phase 2‑A「結案版」

- 已有**明確場景敘述與邊界**：  
  聚焦在「暴力／打架事件的事後調查」，清楚寫出支援與不支援的範圍。
- 已有**至少 3–4 條標準查詢句**，涵蓋：
  - 不同區域：停車場、大門口、樓層走廊、後巷。  
  - 不同時間表述：昨晚、昨天深夜、今天傍晚。
- 每條查詢都具備：
  - `query_id`、`intent`、`text`、`business_description`、`scope_notes`、`required_metadata`、`example_expected_results`。  

接下來 Phase 2‑B / 2‑C 就可以直接用這份 `standard_queries.md`：

- B：為這幾條 query 設計標註與算 Recall@K / Precision@K。  
- C：調整查詢行為與 UI，專心把「打架事件」這個主情境做到可用、可看懂、可量化。
