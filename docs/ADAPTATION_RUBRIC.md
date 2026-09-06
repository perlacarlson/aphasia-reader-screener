# Bilingual Neurogenic Adaptation Rubric (BNAR)
**Proyecto Lectura Accesible: Dual-Language Literature Adaptation for Acquired Alexia & Aphasia**  
*Department of Speech & Hearing Sciences | Portland State University*  
*Framework Standards: UNE 153101:2018 (Lectura Fácil) & Rose et al. (2011/2012)*

---

## 1. Clinical Framework & Theoretical Foundation

This manual establishes the clinical, psycholinguistic, and visuospatial protocols for adapting public-domain literature into accessible dual-language (English/Spanish) reading material for adults with acquired neurogenic reading deficits (aphasia, acquired alexia, right-hemisphere cognitive-communication disorders, and traumatic brain injury).

Standard readability metrics (Flesch-Kincaid, Fernández Huerta) measure surface mechanics (syllables per word, sentence length) but fail to detect neurogenic processing breakdowns such as agrammatic constituent misordering, enclitic masking, and referential ambiguity. The BNAR operationalizes a structured transformation protocol grounded in:
* **The Life Participation Approach to Aphasia (LPAA):** Elevating dignified, age-appropriate cultural literature over infantilizing pediatric materials.
* **Dual Coding Theory (Paivio, 1991):** Integrating non-verbal visual scene anchors with propositional text units to engage preserved right-hemisphere semantic pathways.
* **Supported Conversation for Adults with Aphasia (SCA™, Kagan, 1998):** Utilizing lineation, layout formatting, and multimodal scaffolding to maximize independent comprehension.
* **Bilingual Aphasiology Framework (Paradis, 2011):** Providing bidirectional, parallel language scaffolding to support differential, parallel, or antagonistic recovery patterns.

---

## 2. Morphosyntactic Restructuring Rules (Domain 1)

### 1.1 Canonical Constituent Ordering (S-V-O)
* **Rule:** Reorder all non-canonical patterns (OVS, VSO, fronted adverbials, cleft sentences) into explicit Subject-Verb-Object (SVO) sequences.
* **Clinical Rationale:** Individuals with agrammatic Broca's aphasia or conduction aphasia rely heavily on linear thematic role assignment (Agent $\rightarrow$ Action $\rightarrow$ Theme/Patient).
* **Transformations:**
  * *Original (EN):* *"At the man's heels trotted a dog, a big native husky..."* `[Location-Verb-Subject]`
  * *Adapted (EN):* *"A large dog walked behind the man. The dog was a husky wolf-dog."* `[S-V-O]`
  * *Scaffold (ES):* *"Un perro grande caminaba detrás del hombre. El perro era un husky cruzado con lobo."* `[S-V-O]`

### 1.2 Deconstruction of Enclitic Bundles (Spanish Scaffold)
* **Rule:** Identify all enclitic pronouns attached to infinitives, gerunds, and imperatives. Deconstruct these bundles into independent clauses, overt noun phrases, or analytic modal structures.
* **Clinical Rationale:** Agglutinated clitics obscure verb stems and trigger morphemic parsing breakdowns in deep and phonological alexia.
* **Transformations:**
  * *Agglutinated:* *«...solamente yéndose al monte para curarse...»*
  * *BNAR Target:* *«Él debía ir al bosque. El aire limpio lo iba a curar.»*

### 1.3 Overt Subject Re-specification (Anaphora & Pro-Drop Resolution)
* **Rule:** Invalidate Spanish pro-drop permissions and eliminate ambiguous English pronouns (*he, it, they*). Re-specify the explicit grammatical agent at every episodic transition or clause initiation.
* **Clinical Rationale:** Working-memory constraints impede backward anaphoric tracking across propositional boundaries.
* **Transformations:**
  * *Ambiguous:* *"It knew that it was no time for travelling."*
  * *BNAR Target:* *"The animal knew it was too cold to travel."*
  * *Spanish Scaffold:* *«El animal sabía que era peligroso viajar.»*

### 1.4 Clausal De-Embedding & Coordination
* **Rule:** Eliminate center-embedded and right-branching relative clauses (*who, which, that, que, cuyo*). Split complex conditional and concessive sentences into bounded, coordinated declarative units.
* **Clinical Rationale:** Recursive clause nesting saturates phonological loop capacity and causes immediate syntactic regression.
* **Transformations:**
  * *Original:* *"He paused for breath at the top, excusing the act to himself by looking at his watch."*
  * *BNAR Target:* *"The man stopped to check the time. It was nine o'clock in the morning."*

---

## 3. Lexical, Semantic & Cross-Linguistic Standards (Domain 2)

### 2.1 Concrete Lemma Prioritization & Imageability
* **Rule:** Substitute low-frequency abstract terminology and literary metaphors with high-frequency, concrete lemmas scoring $>5.5$ on standard 7-point concreteness scales.
* **Clinical Rationale:** Acquired reading disorders preferentially preserve access to high-imageability nouns via undamaged sensory-semantic networks.

| Literary Source Lemma | Clinical Substitution (EN) | Parallel Scaffold (ES) | Concreteness Justification |
| :--- | :--- | :--- | :--- |
| *Intangible pall* | *Thick white fog* | *Niebla blanca* | Tangible visual phenomenon vs. abstract noun. |
| *Timberland* | *Forest / Pine trees* | *Bosque / Pinos* | High-frequency concrete natural nouns. |
| *Spittle* | *Spit / Ice* | *Saliva / Hielo* | Tangible physical matter. |
| *Freeze-up* | *Winter ice* | *Hielo de invierno* | Direct physical state. |

### 2.2 Latin American / Mexican Spanish Alignment
* **Rule:** Calibrate the Spanish scaffold to general Latin American / Mexican Spanish norms reflecting regional demographics. Eliminate Peninsular idioms (*coger*, *vosotros*) and archaic regionalisms.
* **Transformations:**
  * *Archaic/Regional:* *Monte* $\rightarrow$ **Bosque** | *Cachorro* $\rightarrow$ **Perro joven**

### 2.3 True Cognate Scaffolding
* **Rule:** Maximize cross-linguistic lexical transfer by prioritizing true English-Spanish cognates within parallel proposition pairs ($>3.0\%$ lexical density).
* **Target Vocabulary:** *Minute / Minuto*, *Distance / Distancia*, *Animal / Animal*, *Danger / Peligro*, *Direction / Dirección*.

### 2.4 Salience Bolding (Visual Anchoring)
* **Rule:** Bold strictly the key lexical **Agent**, primary **Action**, and core **Object/Setting** within each proposition. Never bold grammatical function words (*articles, prepositions, conjunctions*). Limit bolding to 1–3 words per line.
* **Example:** *"The dog was **afraid of the terrible cold**."*

---

## 4. Visuospatial, Typographic & Multimodal Specifications (Domain 3)

| Parameter | Clinical Specification | Aphasiological / Neurogenic Rationale |
| :--- | :--- | :--- |
| **Propositional Lineation** | Exactly **one idea unit** (Subject + Predicate) per line. | Eliminates visual crowding; bounds working-memory intake per visual fixation. |
| **Line Length** | Maximum **45–50 characters** per line (including spaces). | Prevents saccadic drift and tracking loss in concurrent hemianopia or visual neglect. |
| **Margin Alignment** | **Flush-left, ragged-right** (`text-align: left`). Never justified. | Justification creates irregular word spacing ("rivers"), triggering reading disruption. |
| **Typeface & Scale** | Sans-serif (system-ui, Segoe UI, Arial), minimum **18pt (1.15rem)**. | High legibility; eliminates decorative serif friction during letter recognition. |
| **Interline Spacing** | Line-height between **1.8 and 1.9**; paragraph gap $\ge 1.5\times$ line height. | Isolates vertical saccades; prevents line-jumping regressions. |
| **SCA™ Visual Anchors** | Every scene block must include an elevated **68×68px visual anchor tile**. | Dual Coding Theory; provides a non-verbal semantic access route to prime the text. |
| **Bilateral Rail Sync** | Color-coded vertical borders (Green = EN, Blue = ES); cross-hover sync. | Anchors horizontal coordinates during cross-linguistic eye tracking. |

---

## 5. Auditory-Orthographic Verification Protocol (Domain 4)

* **Engine:** Native browser Web Speech API (`window.speechSynthesis`).
* **Calibrated Speech Rate:** Fixed at **0.85x** ($85\%$ of normal speaking rate, $\approx 120\text{–}130\text{ WPM}$) to support auditory comprehension without distorting prosody.
* **Dialect Hierarchy:**
  * **English:** Priority 1: `en-US` (American English — *Samantha*, *Alex*, *Google US English*).
  * **Spanish:** Priority 1: `es-MX` (Mexican Spanish — *Paulina*, *Juan*); Priority 2: `es-US`; Priority 3: `es-419`. Explicitly rejects Peninsular Spanish (`es-ES`) with phonemic *distinción* (/θ/) to avoid phoneme-grapheme confusion.
* **User Agency:** Line-level button triggers ensure user-paced processing rather than continuous passive audio streaming.

---

## 6. Expert Clinician Heuristic Evaluation Protocol (Domain 5)

*Administered to licensed bilingual medical/neuro SLPs during heuristic validation. Evaluated on a 5-point Likert scale (1 = Non-Compliant / Clinical Barrier; 5 = Exemplary Clinical Standard).*

### Scoring Dimensions
1. **Syntactic Transparency:** Strict SVO order; complete clausal de-embedding; elimination of enclitic/passive barriers.
2. **Referential Tracking:** Overt subject naming; zero ambiguous third-person pronouns across propositions.
3. **Lexical Accessibility:** High-imageability lemmas ($>5.5$); regional dialect match; strategic true cognate placement.
4. **Visuospatial Scaffolding:** One proposition per line; $<50$ characters; flush-left/ragged-right; motor-accessible touch targets ($\ge 44\times 44\text{px}$).
5. **Multimodal & Auditory Scaffolding:** SCA™-aligned visual anchor tiles; 0.85x dialect-matched TTS with active visual glow feedback; cross-linguistic hover synchronization.
