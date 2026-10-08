# Learning theory and cognitive extremes

## Verdict

No source examined here establishes an intervention that gives healthy people a large, broad cognitive improvement within minutes to hours and is fully reversible. Exceptional brains establish substantial **task-specific** headroom, not a hidden, general-purpose genius mode. Comparative biology establishes alternative implementations of intelligence, not an acute route to transplant their capabilities into humans.

The strongest leads are computational: improve **which computations are selected, which memories are retrieved, which synapses receive credit, and which old knowledge is protected**, rather than merely increasing activity or plasticity. These are plausible places to look for disproportionate gains. Whether any can produce the full broad-improvement profile is unknown. Rolf can test their computational consequences on his MacBook without a wet lab; he cannot establish a human broad-improvement intervention from those simulations alone.

The most promising near-term research question is whether a controllable change in routing or learning policy can move performance outward across several domains at fixed resources, rather than moving along a trade-off between them. This report proposes tests of that question. It does not claim that the proposed combinations are unprecedented.

## Scope, verification and the standard being applied

This is a targeted literature synthesis, not a systematic review of every relevant publication. It covers computational learning theory; memory, energy and information constraints; corvids and other birds; cephalopods; songbird learning windows; bats; insect cognition; savants and acquired abilities; highly superior autobiographical memory; calculating prodigies; mnemonic and navigation experts; and expert meditators. Molecular interventions, general stimulant headroom and a general public-dataset discovery catalogue belong to the other project reports and are not repeated here.

Every numbered source was opened using curl. For most papers, Europe PMC's core API supplied the bibliographic record and abstract. Where available and needed, its full-text XML supplied methods, limitations or availability statements. The source list distinguishes these levels. An abstract checked against its DOI is not a full-paper appraisal. Several full-text XML requests returned HTTP 500; those papers remain abstract-verified, not full-text-verified. No numerical result below was inferred from a title or recalled from memory.

Coverage of the requested topic categories is complete at the level of a substantive synthesis. Literature coverage within each category is partial. Individual-level data for the rare human cases, comprehensive cross-species cognitive batteries, exhaustive replication histories, and a defensible claim that a hypothesis has never been tried are unavailable in this review. No simulation, reanalysis, human experiment or intervention was performed.

The target remains all of the requested properties together: onset in minutes to hours, full reversibility, large effects, breadth across learning, memory, reasoning and attention, and benefit in healthy people. A large relative change on one difficult puzzle is not evidence of broad enhancement. A neural signal is not a cognitive effect size. Superior performance reached after years of practice is not acute acquisition.

Reversibility needs particular care. Switching a processing state off is different from reversing the memories learned while it was on. Erasing newly acquired knowledge would undermine the learning benefit. The evidence below does not establish full reversibility under either a strict whole-system interpretation or the more practical interpretation of a reversible enhancement state with retained learning. This distinction is not used to relax the brief.

## 1. What learning theory says the bottlenecks might actually be

### Credit assignment: the problem is direction, not just gain

Learning must identify which earlier events, actions and synapses caused an outcome. A stronger update is only useful if it updates the right things. Three-factor learning rules combine local pre- and postsynaptic activity with a later teaching or modulatory signal. An eligibility trace preserves the local event until the teaching signal arrives. Gerstner and colleagues review experimental support for traces bridging neuronal and behavioral timescales [1].

Bellec and colleagues' e-prop provides an explicit computational example: local eligibility traces combined with learning signals can train recurrent spiking networks without ordinary backpropagation through time [2]. The full text says e-prop learns more slowly than backpropagation through time while tending toward its performance. This is not evidence that human brains are inefficient by the same amount, nor that one circulating neuromodulator can deliver an arbitrarily precise error vector.

Spatial assignment matters too. A model with segregated dendritic compartments uses separation of sensory inputs and feedback to coordinate learning across layers [3]. This suggests that missing or badly routed teaching information can constrain learning even when neurons and plasticity machinery are intact. The demonstrated result is in a model, not an enhancement in an adult human.

**Candidate lever:** increase the specificity, timing or contextual relevance of teaching signals, not their indiscriminate strength. A potentially broad mechanism still needs informative feedback in each domain. It cannot teach facts that have not been encountered or identify a correct answer unavailable to the learner. Hypothesis H1 below tests this distinction directly.

### Continual learning: faster learning can destroy useful structure

Complementary learning systems theory explains why rapid episodic storage and slower integration into distributed knowledge can coexist [4]. Slower interleaved learning protects prior structure from new information. This is a computational reason for a brake on learning, not simply a defect of adult brains.

Importantly, the theory does not say all cortical learning must be slow. McClelland and colleagues show that information projecting onto already learned dimensions can be integrated rapidly, whereas genuinely new dimensions require more gradual interleaving [5]. The relevant distinction is **new content within a known model versus a new model**, not merely familiar versus unfamiliar items.

Elastic weight consolidation protects parameters important to previous tasks [6]. Benna and Fusi show how interacting fast and slow synaptic variables can substantially improve memory scaling in a model [7]. Their near-linear capacity scaling is conditional on their architecture and memory assumptions; it is not a count of facts a human can store. Metaplasticity supplies biological mechanisms through which previous activity changes the rules for later plasticity [8].

Modern machine learning also distinguishes forgetting old tasks from losing the ability to learn new ones. Hadsell and colleagues review regularization, modularity, memory and meta-learning approaches [9]. Dohare and colleagues demonstrate loss of plasticity in deep continual-learning settings and show benefits from continually renewing less-used units [10]. That algorithmic result is not evidence for replacing neurons or randomly perturbing a person's brain. It identifies a computational variable—representational diversity—that a model can lose even when ordinary gradient updates remain available.

**Candidate levers:** protect important structure, route new material into appropriate subspaces, preserve useful diversity, and allocate replay to the memories most likely to interfere. These ideas motivate H2 and H9. Any report of faster acquisition must also measure old knowledge, delayed retention and transfer; otherwise increased overwrite can masquerade as enhancement.

### Sparse coding, compression and memory capacity

Olshausen and Field showed that learning sparse codes for natural images can produce receptive-field properties resembling visual cortical simple cells [11]. Sparsity is a way of representing structure efficiently, not a claim that most of the brain is unused. Stronger sparsity can reduce interference and activity costs, but can also discard weak, rare or distributed signals. The optimum depends on the task and input statistics.

Rate-distortion theory makes the trade-off explicit: given a limited channel or memory, retain information whose loss is costly for the task and discard information whose loss is tolerable [12,13]. Bates and colleagues found that visual working-memory performance adapts to stimulus statistics and task-relevant dimensions [14]. This supports flexible allocation, not an unlimited store waiting to be unlocked.

A structural capacity estimate must not be mistaken for usable knowledge. Samavat and colleagues report a synaptic-information estimate with a lower bound of 4.1 bits and an upper bound of 4.59 bits, based on 24 distinguishable spine-size states in their analyzed CA1 material [15]. This is information inferred from anatomical variation under a particular method. Multiplying it by an assumed number of synapses would not establish independently writable, retrievable human memory capacity. Correlations, redundancy, noise, connectivity, interference and the retrieval code all matter.

**Candidate lever:** adapt the representation's precision and sparsity to current demands without permanently discarding information needed elsewhere. H5 asks whether context-dependent allocation beats both globally dense and globally sparse codes. “More detail” and “better abstraction” need not be maximized by the same representation.

### Energy and information limits: constraints, not a numerical impossibility proof

Attwell and Laughlin's energy-budget model made the cost of signaling explicit [16]. Later work revised important allocations after updated estimates of action-potential efficiency. Howarth and colleagues' updated cerebral-cortex model assigns 50% of signaling energy to postsynaptic glutamate receptors and 21% to action potentials [17]. These are model-specific fractions of **signaling** expenditure, not measured fractions of every human brain's entire energy budget. Harris and colleagues review the relation between synaptic computation, energy supply and pathology [18].

The practical inference is that useful computation has energetic and physiological costs. It does not follow that the healthy brain is at a proven global optimum, that supplying more fuel yields more intelligence, or that reducing every source of noise is free. Greater firing, more transmission and longer integration can spend additional resources while producing no useful new information.

Zheng and Meister argue that human behavioral throughput is approximately 10 bits/s despite far larger sensory input rates [19]. This is a provocative synthesis of task-level information rates, not a direct measurement of all internal computation and not an established universal speed limit. Throughput depends on the task, symbol probabilities, training and output requirements. A theory of a narrow behavioral channel cannot be converted into “humans use only a tiny percentage of their brains.”

Resource-rational planning provides a more operational question: given limited computation, which internal calculation is worth doing next? Callaway and colleagues model adaptive planning and compare predictions with human information acquisition [20]. A poor selection policy can waste intact capacity; an apparently suboptimal policy can also be rational under a different internal cost.

**Candidate levers:** improve scheduling, predictive representations or useful information per unit activity. H6 and H10 test these without treating an energy estimate or a model-generated number as a pass criterion. None of these sources quantifies a safe, acute, broad human reserve.

### What machine learning adds—and what it does not

Machine learning supplies constructive examples of separable bottlenecks: representation, optimization, feedback, memory interference, retrieval and allocation of computation. It does not supply a conversion factor from model benchmark gains to human cognitive gains.

Wang and colleagues propose a prefrontal meta-reinforcement-learning system: slow training shapes a recurrent system that can subsequently adapt through its ongoing activity [21]. This matters to the onset requirement. Apparently rapid learning need not mean rapid global rewriting of synaptic weights; it can reflect a previously learned learning procedure operating on new observations. But its apparent speed depends on the prior training and the similarity of the new task to that training.

The Tolman–Eichenbaum machine links structural knowledge to context-specific sensory content, reproducing aspects of spatial and relational representations [22]. It illustrates how a reusable model of relationships can reduce the need to relearn each environment from scratch. It does not prove that applying a spatial code to every reasoning problem will work.

Inference-time adaptation, retrieval, modularity and replay are therefore better hypothesis generators than a generic demand for “more plasticity.” Larger models, more training data or extra computation are not evidence for an acute lever within a fixed human brain. Any proposed computational gain has to reveal which resource was held fixed and whether the improvement survives unfamiliar tasks.

## 2. Comparative biology: different solutions, not a ladder of intelligence

### Corvids, parrots and the bird brain

Olkowicz and colleagues report that parrots and songbirds have, on average, twice as many neurons as primate brains of the same mass, with particularly high pallial allocations in corvids and parrots [23]. This undermines brain mass as a simple proxy for cognitive potential. It does not imply that packing adult human tissue more densely is possible or beneficial.

Stacho and colleagues identify repeated, cortex-like circuit motifs in the avian pallium despite its different large-scale organization [24]. Kabadayi and Osvath report raven planning for tool use and bartering with delays up to 17 hours [25]. The behavioral evidence extends beyond caching, but remains evidence from particular trained tasks, not a common cross-species general-intelligence scale.

There is also a metabolic clue. In pigeons, von Eugen and colleagues estimate per-neuron glucose use at approximately one-third the rate of an average mammalian neuron [26]. This is based on glucose-metabolism measurements and neuron-number estimates, not a matched measurement of identical computations in bird and mammal neurons. It suggests evolutionary alternatives to mammalian energy economics; it does not establish spare metabolic capacity in an adult human.

**Hypothesis contribution:** compact, reusable circuits and efficient communication may matter more than gross volume or indiscriminate activation. H5 and H10 can compare architecture and coding efficiency in models. The observed advantages are evolved/developmental, with no acute onset or reversibility established. Planning breadth in ravens is interesting; broad-improvement breadth in healthy humans remains unestablished.

### Octopus and cuttlefish: associative intelligence through another architecture

The octopus vertical lobe is not a miniature mammalian cortex. Bidel and colleagues reconstruct a small volume of its memory-acquisition network and identify parallel, interconnected feedforward pathways involving simple and complex amacrine cells [27]. Their interpretation distinguishes sparse, memorizable sensory representations from a balancing inhibitory pathway. The study reveals both convergence with other associative systems and a distinctive implementation; the sampled volume is not a complete account of octopus cognition.

Schnell and colleagues report cuttlefish delay maintenance of 50–130 seconds, with better reversal learning in individuals that waited longer [28]. This is a valuable conjunction of self-control and flexible learning in an invertebrate. It does not show human-like general reasoning or a single enhancement factor causing both abilities.

**Hypothesis contribution:** a system may gain useful precision by separating memory-bearing representations from global competition and monitoring. H5 compares these motifs computationally. Feedforward associative capacity should not be confused with the recurrent deliberation needed for every reasoning problem. These are species capabilities, not rapidly reversible enhancements.

The octopus paper explicitly provides a public connectome browser. This review also opened the linked portal and public segmentation metadata [58]. That establishes a real computational entry point. It does not establish that a ready-to-use, synapse-complete graph is supplied, or that reconstructing one from the entire image volume is suitable for Rolf's laptop.

### Songbirds: learning windows are selective protections

Songbirds connect auditory templates, practice, feedback and development in a tractable learning system. Brainard and Doupe describe the sensitive period and the requirement for both tutor exposure and auditory feedback [29]. A template and a period of plasticity are not interchangeable: opening a window does not supply the correct teaching information.

Species differ. Nottebohm and colleagues describe adult canaries' recurring seasonal song instability, acquisition and loss of syllables, and accompanying changes in song-control nuclei [30]. This is important evidence against a universal, once-only closure of adult learning. It is seasonal remodeling, not an hours-scale general enhancement.

Gadagkar and colleagues show that dopamine neurons in singing zebra finches carry performance-error signals relative to internally evaluated song quality [31]. The point for this report is algorithmic: teaching signals can concern an internal target, not just an external reward. Day and colleagues show that changing FoxP2 expression can disturb adult song maintenance in a context-dependent way [32]. These observations make “remove the learning brake” an inadequate description. Plasticity, exploratory variation, feedback and preservation of a learned skill have to be coordinated.

**Hypothesis contribution:** learning windows may protect solutions while reserving selective channels for updating. H1 addresses internal teaching signals; H2 and H9 address stability and plasticity reserve. Transfer to human learning is plausible at a computational level but speculative at an intervention level. Developmental and seasonal timescales fail acute onset; persistent song changes fail simple reversibility; vocal learning is not broad cognition.

### Bats: representation matched to ecological scale

Finkelstein and colleagues find head-direction coding for three-dimensional orientation in bats [33]. Eliav and colleagues record bats flying in a 200-meter tunnel and find place fields ranging from 0.6 to 32 meters, with multiple scales represented within individual neurons [34]. Their decoding analysis supports greater precision across a large environment than comparison codes. Multiscale coding was present from the first day of exposure, including in laboratory-born bats without previous large-environment experience.

That result warns against inferring a universal neural limit from a restricted laboratory task. The measured representation depends on the range of demands presented to it. It does not mean that increasing task scale makes all animals smarter or that the human hippocampus has a bat-specific latent navigation mode.

Bats are also useful for mammalian vocal learning. Vernes and Wilkinson review the comparative evidence [35]; Prat and colleagues show that vocal development depends on auditory exposure in Egyptian fruit bats [36]. The verified primary result concerns development, not an immediate adult boost.

**Hypothesis contribution:** reusable multiscale structure may let a fixed network cover a larger range of problems. H3 tests scale and relational transfer. Ecological specialization and prior development remain essential; acute onset of a useful response is not acute acquisition of the underlying architecture.

### Other small-brain extremes: bees

Howard and colleagues trained honeybees on relative numerosity and found generalization to an empty set at the lower end of the numerical ordering [37]. This is evidence that some apparently sophisticated abstractions can arise in a small nervous system. It is not evidence of symbolic mathematics, unrestricted reasoning, or equivalence with the total cognitive repertoire of a child.

**Hypothesis contribution:** solve a problem with a well-chosen invariant rather than representing every detail. H3 and H5 ask whether structural compression can improve transfer without throwing away information needed by another task. The result also cautions against assuming that every impressive behavior requires a large, human-like architecture.

Across species, selected success stories do not define one shared enhancement direction. Motivation, sensory access, training history, ecological relevance and test design differ. Comparative claims here concern computational motifs, not a ranking of animal intelligence.

## 3. Human extremes: which part of cognition is actually exceptional?

### Congenital savants and pattern-based skill

Treffert's reviews document extraordinary abilities associated with developmental conditions and also distinguish savant syndrome from genius and prodigy [38,39]. Savant syndrome does not imply uniformly low intelligence, and autism is neither necessary nor sufficient for an exceptional skill. Abilities can include creativity rather than mere copying [39].

Mottron and colleagues propose enhanced perceptual processing, pattern detection and completion as contributors to savant performance [43]. This is a theoretical account of how particular representations and interests could support expertise. It competes with, rather than proves, the idea of suppressed abilities waiting intact in everyone.

A key distinction is **more faithful local information versus more useful global abstraction**. Someone can excel at structured material without a corresponding improvement in unrelated reasoning or attention. Persistent focus and practice may also be part of the causal story. The evidence does not isolate a universal, instantly switchable savant mechanism.

### Acquired savant syndrome and the disinhibition hypothesis

Acquired abilities after brain injury or disease are a genuine reason to investigate redistribution of processing. They are not evidence that injury improves cognition overall. In Miller and colleagues' report, five people developed artistic abilities in the setting of frontotemporal dementia; visual skills were spared while language and social skills were severely affected [40]. A new art output can reflect changed motivation, reduced constraint, repetition, altered perception, spared circuitry or some combination. Retrospective cases usually cannot establish that an expert-level representation was present before the event and merely uncovered.

Snyder and colleagues attempted a transient analogue in healthy participants [41]. They reported significant stylistic drawing changes in four of 11 participants, with some proofreading changes. “Stylistic change” is not equivalent to validated artistic mastery, and this small study does not establish a broad cognitive gain.

Chi and Snyder's later sham-controlled insight study included 60 healthy participants and reported that 20% solved an insight problem under sham versus three times as many under one stimulation condition [42]. This is an acute, potentially substantial task-level result and should not be dismissed merely because it is narrow. But it demonstrates neither general reasoning enhancement nor improvements in learning, memory and attention; the abstract does not establish full reversibility or durable benefit. An exhaustive independent replication assessment was not completed here. These studies are cited as hypothesis-generating causal probes, not as a device recommendation or a self-experiment protocol.

**Candidate lever:** selectively weaken an inappropriate prior or semantic template while preserving useful abstraction and error checking. H8 asks whether that can improve unfamiliar problem solving without reciprocal losses. This is the closest human-extreme clue to acute “unlocking,” but among the weaker foundations for broad-improvement claims.

### Hyperthymesia / highly superior autobiographical memory

The original report describes remembering as nonstop, automatic and difficult to control, not as perfect command over all memory [44]. LePort and colleagues studied 11 people with highly superior autobiographical memory (HSAM). They excelled at autobiographical/public events and dates but were comparable with controls on most standard laboratory memory tests [45]. This is direct evidence against treating HSAM as uniformly enhanced memory.

HSAM also does not eliminate reconstruction errors. Patihis and colleagues found susceptibility to associative false memories, misinformation and reports of nonexistent footage [46]. Rich access to one's past can coexist with false recollection. Structural differences in a selected group cannot tell us whether anatomy caused the ability, reflected years of use or tracked another characteristic.

**Candidate lever:** indexing, self-relevance, rehearsal policy or selective long-term retention, rather than indiscriminately stronger initial encoding. H7 compares these alternatives. The observed phenotype is persistent and domain-weighted; neither acute induction nor reversibility has been established. More autobiographical recall is not automatically better reasoning or a more controllable mind.

### Calculating prodigies and extreme expertise

Pesenti and colleagues' PET study of a calculating prodigy suggests use of an alternative strategy involving episodic memory and different neural recruitment, rather than a simple amplification of the same processes used by non-experts [47]. A single expert does not resolve the relative roles of predisposition, practice and strategy. The result nevertheless points to **algorithm selection and access to long-term structures** as a plausible source of disproportionate performance.

Maguire and colleagues found that superior memorizers used spatial strategies, without exceptional general intellectual ability or structural brain differences explaining their memory feats [48]. Dresler and colleagues examined 23 memory athletes and found that six weeks of mnemonic training in initially untrained people shifted functional connectivity toward athlete-like organization; similarity predicted memory improvements up to four months later [49]. That is evidence for learnable access to exceptional domain performance. Six weeks is not minutes to hours, and a persistent training benefit is not a reversible state.

Navigation expertise gives an additional caution. Woollett and Maguire followed London taxi trainees over four years and found posterior hippocampal structural changes in those who qualified [50]. Their full text also reports worse delayed complex-figure recall in qualified trainees relative to controls at follow-up. The point is not that every expertise gain must impose a cost, but that a positive result on the trained skill cannot establish an across-domain improvement.

Sala and Gobet's synthesis of chess, music and working-memory training finds that more rigorous designs yield smaller effects, and concludes that far transfer is rare [54]. This does not prove that broad transfer is impossible. It makes domain-specific strategy a stronger explanation than a generally increased cognitive capacity for many existing training successes.

**Candidate lever:** route a task into an already powerful learned representation or retrieval procedure. H4 tests this directly; H3 asks whether reusable structure can extend transfer. These are unusually strong examples of real, healthy-human headroom, but weak examples of acute, broad, reversible headroom.

### Expert meditators: trainable allocation is not superintelligence

Lutz and colleagues report that long-term practitioners can self-induce high-amplitude gamma synchrony during meditation, with differences also present at baseline and afterwards [51]. This is evidence about brain state and training history. Gamma amplitude is not a validated scale of intelligence, learning speed or reasoning quality; the observational expert comparison cannot isolate training from selection.

Slagter and colleagues found a smaller attentional blink after three months of intensive training, alongside reduced allocation to the first target [52]. The full text describes a practitioner group and a comparison group, rather than a randomized allocation of everyone to intensive retreat. Participants were not formally meditating during the attention task. This is a specific example in which **less processing devoted to one event** accompanies better subsequent processing, not evidence that more neural activity is better.

Whitfield and colleagues' meta-analysis included 56 studies, with 45 synthesized quantitatively. The pooled cognitive effect was small: Hedges' g = 0.15, with interval [0.05, 0.24]. Benefits were seen against inactive, but not active, comparators [53]. That meta-analysis concerns mindfulness-based programs, not every extreme contemplative tradition; it nevertheless weighs against treating established training effects as large general enhancement.

**Candidate lever:** alter attentional dwell time, distractor capture or metacontrol so that intact resources are used more efficiently. This contributes to H6. Expert state entry can be rapid after long training, but its broad benefit, magnitude and complete reversibility are not established. Learning to enter the state and the effect of entering it must be separated.

## 4. Falsifiable dry-lab hypotheses

These are proposed studies, not results. All can begin with equations, synthetic tasks or openly published aggregate results; none requires privileged clinical records, an institutional application, a wet lab or intervention on Rolf. Small models are the appropriate starting point on his M5 Pro MacBook with 24 GB. Full-scale connectomics, frontier-model training and exhaustive reproductions of large published benchmarks are not assumed feasible. Runtime and memory use have not been benchmarked.

For all hypotheses, compare models with matched observations, training opportunity and relevant computational resources. Report acquisition, retention, response time or computation, errors and transfer separately. Evaluate unfamiliar task structures as well as familiar ones. In model comparisons, “switching off” means testing return of the operating policy, not silently resetting learned weights. A model improvement is evidence for a possible computation, not evidence of human efficacy.

### H1. The bottleneck is misassigned credit, not insufficient plasticity

**Basis:** eligibility traces, compartmentalized feedback and songbird performance errors [1–3,31].

**Test:** implement a small recurrent learner on delayed-feedback sequence, classification and decision tasks. Compare uniform gain changes with better-timed and better-targeted teaching signals while holding total update magnitude or update budget comparable. Vary delay, misleading feedback and task switches. Use the public e-prop implementation as a reference [55], not as proof that a particular biological mechanism is present in humans.

**Discriminating outcome:** specificity improves learning and retention across task families while gain mainly increases instability. If benefits vanish after update budget and prior information are matched, or require an omniscient teacher unavailable to the brain, the proposed explanation weakens.

**Speculation and profile fit:** strong basis for the computational problem; moderate speculation that addressability is a major human bottleneck; very high speculation that it is acutely and broadly controllable. Signal timing can operate rapidly, but acquired changes can persist. Large, broad, reversible healthy-human benefit is unestablished.

### H2. Selective interference protection permits faster learning without erasure

**Basis:** complementary learning systems, task-selective stabilization and multiscale synaptic memory [4–7,9].

**Test:** train sequentially on tasks with known shared and conflicting components. Compare a globally increased learning rate, protected important parameters, modular updates and targeted replay at equal storage and replay budgets. Include information that fits an existing schema and information requiring a genuinely new dimension. Measure old-task retention as well as acquisition and relational transfer.

**Discriminating outcome:** selective protection improves the joint acquisition–retention frontier, not just one side. Failure on newly structured tasks would support a narrower schema-access explanation rather than general acceleration. Extra hidden storage or replay must not account for the result.

**Speculation and profile fit:** well-grounded computationally; uncertain biological control. It could accelerate learning over exposures, but cannot instantly provide missing knowledge. The learned content persists, and breadth across attention and reasoning is not established. No acute reversible human implementation is demonstrated.

### H3. Apparent rapid intelligence reflects reuse of structural priors

**Basis:** meta-reinforcement learning, the Tolman–Eichenbaum machine, bat multiscale coding and bee generalization [21,22,34,37].

**Test:** pretrain a compact recurrent or relational model on a family of graphs and tasks. Test new instances, changed scale and genuinely changed rules. Compare fixed-weight inference-time adaptation against new weight learning. Use graph navigation, relational inference and sequence prediction so that success cannot be explained by one sensory interface. The published TEM code is public [56]; a small reimplementation can avoid obsolete dependencies.

**Discriminating outcome:** reusable structure supports broad transfer within and beyond the pretraining family without accessing additional answers. A collapse outside the familiar family would show powerful specialization, not general acceleration. Count the pretraining cost rather than treating it as free.

**Speculation and profile fit:** plausible explanation of fast adaptation; speculative general-purpose human lever. A latent procedure could be recruited quickly, but availability and quality of that procedure constrain the result. Reversibility of a model's context state does not establish reversibility of a human enhancement.

### H4. Retrieval and indexing, rather than storage size, constrain exceptional performance

**Basis:** calculating expertise, spatial mnemonics and training-induced memory-network changes [47–49].

**Test:** give different models identical stored content and vary only indexing, chunk organization and retrieval policy. Compare associative retrieval, list recall, multistep arithmetic and relational reasoning. Track incorrect retrievals and the computational cost of finding useful content. Contrasting intact versus scrambled task structure tests whether a gain depends on expert chunks. Synthetic content is sufficient; private prodigy data are not needed.

**Discriminating outcome:** better indexing yields gains in several domains without enlarging the knowledge base or using a hidden solution oracle. A memory gain with unchanged reasoning, or a gain that requires laboriously built domain-specific chunks, supports a real but domain-specific form of headroom.

**Speculation and profile fit:** strong evidence for strategy-sensitive human performance; moderate speculation about a shared indexing bottleneck. Switching retrieval policy might be acute once learned. Existing exceptional strategies took training, do not establish broad attention gains and are not fully reversible enhancements.

### H5. Context-dependent compression beats uniformly more detail or more sparsity

**Basis:** sparse coding, rate-distortion models, adaptive working memory, savant pattern accounts and octopus circuitry [11–14,27,43].

**Test:** compare dense, fixed-sparse and context-adaptive representations under matched representational and activity budgets. Include local-detail discrimination, category abstraction, rare-event detection and associative recall. Test an octopus-inspired split between sparse memory-bearing pathways and global competition; compare it with simpler controls, not only a weak baseline. Published motifs suffice initially; the public octopus data can later constrain anatomy [58].

**Discriminating outcome:** adaptive allocation improves several objectives rather than trading detail for abstraction. If a controller needs to know the correct answer to choose its code, or gains vanish on unexpected changes in relevance, the proposed lever is much weaker.

**Speculation and profile fit:** established principles of coding; speculative controllable human representation policy. Policy changes can be rapid in a model, but remapping learned representations may not be. Large broad healthy-human benefit and full reversibility are not established.

### H6. Cognitive throughput is limited partly by scheduling and overcommitment

**Basis:** resource-rational planning, the behavioral-bandwidth hypothesis and attentional-blink results [19,20,51–53].

**Test:** compare serial schedulers, adaptive dwell-time policies and bounded parallel workers with the same total processing budget. Use paired-target detection, working-memory updating and planning under distraction. Fit only publicly reported aggregate behavioral patterns unless trial-level data are independently verified. Include speed–accuracy and first-task–second-task trade-offs; do not equate a faster response with greater information throughput.

**Discriminating outcome:** a shared scheduler improves several tasks without simply lowering decision thresholds or neglecting the first target. If better performance requires extra parallel compute, more prior knowledge or a slower response, it does not establish a released scheduling reserve at fixed resources.

**Speculation and profile fit:** plausible and computationally accessible; the size of avoidable inefficiency in healthy humans is unknown. A control policy can, in principle, change quickly and be switched back, making this relatively close to the onset/reversibility shape. Existing meditation evidence falls far short on magnitude and breadth.

### H7. HSAM reflects retention or access policy, not a general encoding multiplier

**Basis:** autobiographical selectivity and preserved susceptibility to false memory [44–46].

**Test:** simulate an episodic memory stream with dates, personal relevance, interference and repeated retrieval. Compare increased initial encoding precision, context-rich indexing, selective rehearsal and slower forgetting. Ask which can reproduce high autobiographical access alongside ordinary laboratory recall and false recognition. Use source-reported group patterns as constraints, not as synthetic individual-level measurements.

**Discriminating outcome:** a selective retention/access model reproduces the dissociations without predicting universal memory superiority. If several models do equally well, report non-identifiability rather than selecting a mechanism by preference. Rare-case raw longitudinal data were not verified here, so human mechanism identification remains limited.

**Speculation and profile fit:** useful explanation test; weak route to the target. The phenotype develops over time, concerns selected memories and is not known to be switchable. Increasing retention could increase unwanted accessibility rather than reasoning or control.

### H8. Controlled relaxation of priors can expose useful detail without losing abstraction

**Basis:** acquired artistic abilities, perceptual accounts of savant skills and small acute stimulation studies [40–43].

**Test:** use hierarchical models with tunable top-down constraint. Evaluate misleading-context problems, detail detection, ambiguity resolution and ordinary semantic inference together. Compare reversible policy changes with actual information loss or simulated lesions. Existing published task results can define the problem classes; do not infer stimulation mechanisms from a model parameter.

**Discriminating outcome:** a context-sensitive gate improves misleading-prior tasks while preserving ordinary inference and calibration. If all gains require reciprocal damage, the model supports specialization or paradoxical facilitation, not broad enhancement. A global reduction in prior influence should face the strongest ordinary-context controls.

**Speculation and profile fit:** human task-level acute clues exist, but broad interpretation is highly speculative. Disease cases fail the healthy-person and reversibility requirements; small stimulation studies do not establish magnitude across domains or full reversal. No injury or stimulation procedure is proposed.

### H9. Preserving representational diversity is different from globally reopening plasticity

**Basis:** metaplasticity, loss of plasticity in artificial networks and songbird maintenance/update dynamics [8–10,29–32].

**Test:** in a compact continually learning model, independently vary stability of important parameters, diversity of less-used representations and global update rate. Distinguish retention of old tasks from acquisition of new ones. Include changing task distributions so that a dormant representation can later become useful. The loss-of-plasticity code is public [57], but its large benchmarks need not be reproduced to test this narrow hypothesis.

**Discriminating outcome:** diversity-preserving methods recover acquisition without sacrificing established knowledge. If improvement merely replaces old competence with new competence, or works only by adding capacity, it does not support an unused reserve.

**Speculation and profile fit:** model evidence is substantial; analogy to human adult learning windows is speculative. Biological restructuring would likely differ from switching an activity policy, and the sources do not establish an acute, reversible implementation. Breadth is principally learning, not immediate general reasoning.

### H10. Communication efficiency matters more than raising the total activity budget

**Basis:** revised energy budgets, bird neuron packing and pigeon neuronal glucose estimates [16–18,23,24,26].

**Test:** compare compact versus long-range architectures and sparse versus dense signaling on matched tasks. Charge separately for messages, synaptic events, maintained states and computation; vary those cost assumptions instead of declaring an artificial-unit count equivalent to ATP. Ask whether efficient routing preserves precision and transfer under noise and delay. Published energy estimates provide sensitivity ranges, not a single exact human cost model.

**Discriminating outcome:** an architecture or policy needs less communication for equivalent task performance, and retains that advantage under plausible alternative accounting. If the result depends on ignoring maintenance or long-range communication, it is an accounting artifact rather than a biological lead.

**Speculation and profile fit:** energy constraints are real; cross-species transfer is highly speculative. Evolved packing and wiring cannot be acutely installed in a healthy adult. A routing policy might be adjustable, but no measured source here establishes a large reversible reserve from it. This is a useful constraint on other hypotheses, not the closest direct broad-improvement route.

## 5. What public computation can and cannot settle

The executable starting points are real but not turn-key evidence. The e-prop authors' repository and README were opened; the README specifies older TensorFlow and Python versions and recommends Linux [55]. Its existence is not evidence that it will run unchanged on an Apple-silicon Mac. Reimplementing its small learning-rule examples is a more bounded first step than attempting its speech or game benchmarks.

The TEM and loss-of-plasticity repositories were confirmed public via GitHub metadata [56,57]. They were not installed or executed. The octopus portal and cloud segmentation metadata were opened [58]; the metadata exposes chunked multiresolution segmentation. Full image analysis, synapse extraction and construction of a biological adjacency graph are separate projects. Start with the published motifs, not an unbounded image download.

A feasible first deliverable would be a compact benchmark comparison among better credit routing (H1), selective interference protection (H2) and context-adaptive scheduling or representation (H5/H6). It should make resource accounting and negative transfer visible. This is not a replacement goal for broad improvement; it is a way to reject attractive explanations before making human claims.

The hardest missing evidence is causal access. A successful simulation can establish that a proposed computation is sufficient under its assumptions. It cannot establish that healthy human brains have the corresponding unused reserve, that a non-invasive control variable reaches it, or that switching it produces a large and broad benefit without persistent changes. Rare cases and species comparisons do not supply those missing links.

## 6. Ranked leads closest to the full broad-improvement profile

This is an ordinal judgment about resemblance to the requested profile, not a probability estimate or a list of validated interventions. None meets all the requirements.

1. **Adaptive metacontrol and resource scheduling (H6, with H5).** Closest in principle to rapid state change and switchability, with possible reach across multiple computations. The observed human attention and mindfulness effects do not establish large broad benefits. A reversible control policy is more plausible than acute anatomical redesign; its headroom is unknown.
2. **Recruitment of latent strategies and reusable representations (H3/H4).** Strongest evidence that healthy people can reach exceptional domain performance using existing brain machinery. Acute deployment is distinguishable from the long training needed to build it. Broad transfer and full reversibility are missing.
3. **More precise credit assignment plus interference protection (H1/H2).** Strong computational case for improving learning without just amplifying updates. Potentially relevant to several learning domains, but dependent on informative feedback and accumulated experience. Immediate reasoning/attention gains and reversible memory changes are not established.
4. **Selective relaxation of unhelpful priors (H8).** Has acute healthy-human task-level clues, including a large relative insight-task result. Evidence quality and breadth are weaker than the appeal of an “unlocking” story; acquired-savant cases show why losses must be measured. Full reversibility is not established.
5. **Metaplasticity and preserved representational diversity (H9).** A serious continual-learning lead, supported by learning theory and comparative biology. Poor match to acute onset and complete reversal; no demonstrated healthy-human general enhancement.
6. **HSAM-like retention/access policies (H7).** A real extreme memory phenotype, but autobiographically selective, persistent and sometimes intrusive. It is not broad intelligence or a demonstrated acute state.
7. **Avian-like efficiency or alternative associative architecture (H10 and octopus-inspired H5).** Powerful evidence that current human anatomy is not the only possible implementation of cognition. Weakest near-term match to a reversible adult-human intervention because the observed advantages largely concern development and architecture.

## 7. Ranked hypotheses most testable by Rolf now

The ranking below concerns testability with public computation, not likelihood of producing broad improvement. All remain proposals.

1. **H1: credit specificity versus global gain.** Public reference implementation; small synthetic delayed-feedback tasks; a direct comparison that can falsify the simplest “more plasticity” account.
2. **H2: interference-selective fast learning.** Straightforward sequential-task simulations; explicit acquisition–retention trade-off; no privileged biological data required.
3. **H5: adaptive compression and sparsity.** Small synthetic tasks can expose detail–abstraction trade-offs and hidden resource subsidies; biological motifs offer constraints rather than promises.
4. **H4: retrieval and indexing.** Hold content fixed and change retrieval policy. This cleanly separates stored information from usable performance and connects to documented healthy-human expertise.
5. **H3: structural reuse and inference-time adaptation.** Public model reference and synthetic relational environments; harder to distinguish truly broad transfer from a favorable pretraining family.
6. **H9: diversity preservation versus plasticity gain.** Public reference code and measurable forgetting/acquisition dissociations; biological interpretation remains a second, unresolved step.
7. **H6: scheduling and overcommitment.** Easy to simulate, harder to identify uniquely from human aggregate data. It ranks higher for broad-improvement resemblance than for decisive mechanism identification.
8. **H8: detail access through selective prior relaxation.** Feasible model comparison with important reciprocal-cost tests; mapping the parameter to savant cases or stimulation effects is highly uncertain.
9. **H10: energy-aware communication efficiency.** Feasible sensitivity analysis but strongly dependent on cost accounting and unknown cross-species comparability; cannot quantify a human reserve.
10. **H7: HSAM retention versus access.** Qualitative dissociations are available, but lack of verified longitudinal individual-level data makes multiple explanations difficult to separate.

A negative result is useful here. If candidate controllers merely reshuffle errors, model speedups rely on hidden pretraining, or better learning requires irreversible rewriting, that directly narrows the path to the original acute, reversible, large and broad goal. It does not justify renaming a narrower success “broad improvement.”

## Sources and verification record

**Verified—A** means bibliographic metadata and abstract opened through the Europe PMC core API (`https://www.ebi.ac.uk/europepmc/webservices/rest/search`, using title/author queries and `resultType=core`). **Verified—F** additionally means full-text XML opened and relevant sections inspected at `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML`. Neither label implies independent replication or data reanalysis. **Verified—R** identifies an opened resource. All sources cited in the report are verified at the stated level; full texts not inspected must not be treated as full-text-verified.

### Learning theory, computation and constraints

[1] Gerstner W et al. (2018). “Eligibility Traces and Plasticity on Behavioral Time Scales: Experimental Support of NeoHebbian Three-Factor Learning Rules.” *Frontiers in Neural Circuits*. DOI: https://doi.org/10.3389/fncir.2018.00053. PMID 30108488; PMC6079224. **Verified—F.** Theory/experimental-evidence review.

[2] Bellec G et al. (2020). “A solution to the learning dilemma for recurrent networks of spiking neurons.” *Nature Communications*. DOI: https://doi.org/10.1038/s41467-020-17236-y. PMID 32681001; PMC7367848. **Verified—F.** Computational model; methods and code statement checked.

[3] Guerguiev J, Lillicrap TP, Richards BA (2017). “Towards deep learning with segregated dendrites.” *eLife*. DOI: https://doi.org/10.7554/eLife.22901. PMID 29205151. **Verified—A.** Computational model.

[4] McClelland JL, McNaughton BL, O'Reilly RC (1995). “Why there are complementary learning systems in the hippocampus and neocortex: insights from the successes and failures of connectionist models of learning and memory.” *Psychological Review*. DOI: https://doi.org/10.1037/0033-295X.102.3.419. PMID 7624455. **Verified—A.** Theory.

[5] McClelland JL, McNaughton BL, Lampinen AK (2020). “Integration of new information in memory: new insights from a complementary learning systems perspective.” *Philosophical Transactions B*. DOI: https://doi.org/10.1098/rstb.2019.0637. PMID 32248773. **Verified—A.** Computational theory.

[6] Kirkpatrick J et al. (2017). “Overcoming catastrophic forgetting in neural networks.” *PNAS*. DOI: https://doi.org/10.1073/pnas.1611835114. PMID 28292907. **Verified—A.** Machine-learning experiments.

[7] Benna MK, Fusi S (2016). “Computational principles of synaptic memory consolidation.” *Nature Neuroscience*. DOI: https://doi.org/10.1038/nn.4401. PMID 27694992. **Verified—A.** Memory-capacity model.

[8] Abraham WC (2008). “Metaplasticity: tuning synapses and networks for plasticity.” *Nature Reviews Neuroscience*. DOI: https://doi.org/10.1038/nrn2356. PMID 18401345. **Verified—A.** Review.

[9] Hadsell R et al. (2020). “Embracing Change: Continual Learning in Deep Neural Networks.” *Trends in Cognitive Sciences*. DOI: https://doi.org/10.1016/j.tics.2020.09.004. PMID 33158755. **Verified—A.** Review.

[10] Dohare S et al. (2024). “Loss of plasticity in deep continual learning.” *Nature*. DOI: https://doi.org/10.1038/s41586-024-07711-7. PMID 39169245; PMC11338828. **Verified—F.** Machine-learning experiments; code statement checked.

[11] Olshausen BA, Field DJ (1996). “Emergence of simple-cell receptive field properties by learning a sparse code for natural images.” *Nature*. DOI: https://doi.org/10.1038/381607a0. PMID 8637596. **Verified—A.** Computational model.

[12] Sims CR (2016). “Rate-distortion theory and human perception.” *Cognition*. DOI: https://doi.org/10.1016/j.cognition.2016.03.020. PMID 27107330. **Verified—A.** Theory/modeling.

[13] Sims CR, Jacobs RA, Knill DC (2012). “An ideal observer analysis of visual working memory.” *Psychological Review*. DOI: https://doi.org/10.1037/a0029856. PMID 22946744. **Verified—A.** Model and behavioral tests.

[14] Bates CJ et al. (2019). “Adaptive allocation of human visual working memory capacity during statistical and categorical learning.” *Journal of Vision*. DOI: https://doi.org/10.1167/19.2.11. PMID 30802280. **Verified—A.** Behavioral experiments/model.

[15] Samavat M et al. (2024). “Synaptic Information Storage Capacity Measured With Information Theory.” *Neural Computation*. DOI: https://doi.org/10.1162/neco_a_01659. PMID 38658027. **Verified—A.** Anatomical information-capacity analysis; not a human cognitive capacity estimate.

[16] Attwell D, Laughlin SB (2001). “An energy budget for signaling in the grey matter of the brain.” *Journal of Cerebral Blood Flow & Metabolism*. DOI: https://doi.org/10.1097/00004647-200110000-00001. PMID 11598490. **Verified—A.** Energy-budget model.

[17] Howarth C, Gleeson P, Attwell D (2012). “Updated energy budgets for neural computation in the neocortex and cerebellum.” *Journal of Cerebral Blood Flow & Metabolism*. DOI: https://doi.org/10.1038/jcbfm.2012.35. PMID 22434069. **Verified—A.** Revised energy-budget models.

[18] Harris JJ, Jolivet R, Attwell D (2012). “Synaptic energy use and supply.” *Neuron*. DOI: https://doi.org/10.1016/j.neuron.2012.08.019. PMID 22958818. **Verified—A.** Review.

[19] Zheng J, Meister M (2025; online 2024). “The unbearable slowness of being: Why do we live at 10 bits/s?” *Neuron*. DOI: https://doi.org/10.1016/j.neuron.2024.11.008. PMID 39694032. **Verified—A.** Theoretical synthesis; full-text XML request failed.

[20] Callaway F et al. (2022). “Rational use of cognitive resources in human planning.” *Nature Human Behaviour*. DOI: https://doi.org/10.1038/s41562-022-01332-8. PMID 35484209. **Verified—A.** Computational model and behavioral experiment.

[21] Wang JX et al. (2018). “Prefrontal cortex as a meta-reinforcement learning system.” *Nature Neuroscience*. DOI: https://doi.org/10.1038/s41593-018-0147-8. PMID 29760527. **Verified—A.** Computational theory.

[22] Whittington JCR et al. (2020). “The Tolman-Eichenbaum Machine: Unifying Space and Relational Memory through Generalization in the Hippocampal Formation.” *Cell*. DOI: https://doi.org/10.1016/j.cell.2020.10.024. PMID 33181068; PMC7707106. **Verified—F.** Model with neural-data comparisons; code availability checked.

### Comparative biology

[23] Olkowicz S et al. (2016). “Birds have primate-like numbers of neurons in the forebrain.” *PNAS*. DOI: https://doi.org/10.1073/pnas.1517131113. PMID 27298365. **Verified—A.** Comparative anatomy; full-text XML request failed.

[24] Stacho M et al. (2020). “A cortex-like canonical circuit in the avian forebrain.” *Science*. DOI: https://doi.org/10.1126/science.abc5534. PMID 32973004. **Verified—A.** Comparative circuit anatomy.

[25] Kabadayi C, Osvath M (2017). “Ravens parallel great apes in flexible planning for tool-use and bartering.” *Science*. DOI: https://doi.org/10.1126/science.aam8138. PMID 28706072. **Verified—A.** Animal behavioral experiments.

[26] von Eugen K et al. (2022). “Avian neurons consume three times less glucose than mammalian neurons.” *Current Biology*. DOI: https://doi.org/10.1016/j.cub.2022.07.070. PMID 36084646. **Verified—A.** Pigeon metabolism study and comparative estimate.

[27] Bidel F et al. (2023). “Connectomics of the Octopus vulgaris vertical lobe provides insight into conserved and novel principles of a memory acquisition network.” *eLife*. DOI: https://doi.org/10.7554/eLife.84257. PMID 37410519; PMC10325715. **Verified—F.** Volume electron microscopy; public-data statement checked.

[28] Schnell AK et al. (2021). “Cuttlefish exert self-control in a delay of gratification task.” *Proceedings of the Royal Society B*. DOI: https://doi.org/10.1098/rspb.2020.3161. PMID 33653135. **Verified—A.** Animal behavioral experiments; full-text XML request failed.

[29] Brainard MS, Doupe AJ (2002). “What songbirds teach us about learning.” *Nature*. DOI: https://doi.org/10.1038/417351a. PMID 12015616. **Verified—A.** Review.

[30] Nottebohm F, Nottebohm ME, Crane L (1986). “Developmental and seasonal changes in canary song and their relation to changes in the anatomy of song-control nuclei.” *Behavioral and Neural Biology*. DOI: https://doi.org/10.1016/S0163-1047(86)90485-1. PMID 3814048. **Verified—A.** Longitudinal/comparative behavioral anatomy.

[31] Gadagkar V et al. (2016). “Dopamine neurons encode performance error in singing birds.” *Science*. DOI: https://doi.org/10.1126/science.aah6837. PMID 27940871. **Verified—A.** Recording and auditory-feedback experiment.

[32] Day NF et al. (2019). “Beyond Critical Period Learning: Striatal FoxP2 Affects the Active Maintenance of Learned Vocalizations in Adulthood.” *eNeuro*. DOI: https://doi.org/10.1523/ENEURO.0071-19.2019. PMID 31001575. **Verified—A.** Animal perturbation study.

[33] Finkelstein A et al. (2015). “Three-dimensional head-direction coding in the bat brain.” *Nature*. DOI: https://doi.org/10.1038/nature14031. PMID 25470055. **Verified—A.** Neural recordings.

[34] Eliav T et al. (2021). “Multiscale representation of very large environments in the hippocampus of flying bats.” *Science*. DOI: https://doi.org/10.1126/science.abg4020. PMID 34045327. **Verified—A.** Neural recordings and decoding analysis.

[35] Vernes SC, Wilkinson GS (2020). “Behaviour, biology and evolution of vocal learning in bats.” *Philosophical Transactions B*. DOI: https://doi.org/10.1098/rstb.2019.0061. PMID 31735153. **Verified—A.** Review; full-text XML request failed.

[36] Prat Y, Taub M, Yovel Y (2015). “Vocal learning in a social mammal: Demonstrated by isolation and playback experiments in bats.” *Science Advances*. DOI: https://doi.org/10.1126/sciadv.1500019. PMID 26601149. **Verified—A.** Developmental animal experiment.

[37] Howard SR et al. (2018). “Numerical ordering of zero in honey bees.” *Science*. DOI: https://doi.org/10.1126/science.aar4975. PMID 29880690. **Verified—A.** Animal behavioral experiments.

### Human exceptional cognition and transfer

[38] Treffert DA (2009). “The savant syndrome: an extraordinary condition. A synopsis: past, present, future.” *Philosophical Transactions B*. DOI: https://doi.org/10.1098/rstb.2008.0326. PMID 19528017. **Verified—A.** Clinical review; full-text XML request failed.

[39] Treffert DA (2014). “Savant syndrome: realities, myths and misconceptions.” *Journal of Autism and Developmental Disorders*. DOI: https://doi.org/10.1007/s10803-013-1906-8. PMID 23918440. **Verified—A.** Review.

[40] Miller BL et al. (1998). “Emergence of artistic talent in frontotemporal dementia.” *Neurology*. DOI: https://doi.org/10.1212/WNL.51.4.978. PMID 9781516. **Verified—A.** Clinical case series.

[41] Snyder AW et al. (2003). “Savant-like skills exposed in normal people by suppressing the left fronto-temporal lobe.” *Journal of Integrative Neuroscience*. DOI: https://doi.org/10.1142/S0219635203000287. PMID 15011267. **Verified—A.** Small exploratory stimulation study.

[42] Chi RP, Snyder AW (2011). “Facilitate insight by non-invasive brain stimulation.” *PLOS ONE*. DOI: https://doi.org/10.1371/journal.pone.0016655. PMID 21311746. **Verified—A.** Sham-controlled task experiment; full replication history not established here.

[43] Mottron L, Dawson M, Soulières I (2009). “Enhanced perception in savant syndrome: patterns, structure and creativity.” *Philosophical Transactions B*. DOI: https://doi.org/10.1098/rstb.2008.0333. PMID 19528021. **Verified—A.** Theoretical account/review.

[44] Parker ES, Cahill L, McGaugh JL (2006). “A case of unusual autobiographical remembering.” *Neurocase*. DOI: https://doi.org/10.1080/13554790500473680. PMID 16517514. **Verified—A.** Single case.

[45] LePort AK et al. (2012). “Behavioral and neuroanatomical investigation of Highly Superior Autobiographical Memory (HSAM).” *Neurobiology of Learning and Memory*. DOI: https://doi.org/10.1016/j.nlm.2012.05.002. PMID 22652113. **Verified—A.** Behavioral and structural imaging study; full-text XML request failed.

[46] Patihis L et al. (2013). “False memories in highly superior autobiographical memory individuals.” *PNAS*. DOI: https://doi.org/10.1073/pnas.1314373110. PMID 24248358. **Verified—A.** Behavioral comparison.

[47] Pesenti M et al. (2001). “Mental calculation in a prodigy is sustained by right prefrontal and medial temporal areas.” *Nature Neuroscience*. DOI: https://doi.org/10.1038/82831. PMID 11135652. **Verified—A.** Expert case with comparison-group PET.

[48] Maguire EA et al. (2003). “Routes to remembering: the brains behind superior memory.” *Nature Neuroscience*. DOI: https://doi.org/10.1038/nn988. PMID 12483214. **Verified—A.** Expert comparison with imaging.

[49] Dresler M et al. (2017). “Mnemonic Training Reshapes Brain Networks to Support Superior Memory.” *Neuron*. DOI: https://doi.org/10.1016/j.neuron.2017.02.003. PMID 28279356. **Verified—A.** Expert comparison and mnemonic-training study; full-text XML request failed.

[50] Woollett K, Maguire EA (2011). “Acquiring ‘the Knowledge’ of London's layout drives structural brain changes.” *Current Biology*. DOI: https://doi.org/10.1016/j.cub.2011.11.018. PMID 22169537; PMC3268356. **Verified—F.** Longitudinal naturalistic study; complex-figure recall result checked in full text.

[51] Lutz A et al. (2004). “Long-term meditators self-induce high-amplitude gamma synchrony during mental practice.” *PNAS*. DOI: https://doi.org/10.1073/pnas.0407401101. PMID 15534199. **Verified—A.** Expert EEG comparison.

[52] Slagter HA et al. (2007). “Mental training affects distribution of limited brain resources.” *PLOS Biology*. DOI: https://doi.org/10.1371/journal.pbio.0050138. PMID 17488185; PMC1865565. **Verified—F.** Longitudinal attention/EEG study; participant groups and task state checked.

[53] Whitfield T et al. (2022; online 2021). “The Effect of Mindfulness-based Programs on Cognitive Function in Adults: A Systematic Review and Meta-analysis.” *Neuropsychology Review*. DOI: https://doi.org/10.1007/s11065-021-09519-y. PMID 34350544; PMC9381612. **Verified—F.** Meta-analysis; active-comparator and risk-of-bias limitations checked.

[54] Sala G, Gobet F (2017). “Does Far Transfer Exist? Negative Evidence From Chess, Music, and Working Memory Training.” *Current Directions in Psychological Science*. DOI: https://doi.org/10.1177/0963721417712760. PMID 29276344. **Verified—A.** Meta-analytic synthesis.

### Computational resources actually opened

[55] Official e-prop repository: https://github.com/IGITUGraz/eligibility_propagation. **Verified—R.** GitHub repository API returned public metadata; raw README opened at https://raw.githubusercontent.com/IGITUGraz/eligibility_propagation/master/README.md. This verifies availability and documented dependencies, not local execution.

[56] TEM repository: https://github.com/djcrw/generalising-structural-knowledge. **Verified—R.** Linked by [22]; GitHub repository API returned public metadata. No local execution or dependency validation.

[57] Loss-of-plasticity repository: https://github.com/shibhansh/loss-of-plasticity. **Verified—R.** Linked by [10]; GitHub repository API returned public metadata. No local execution or benchmark reproduction.

[58] Octopus connectome portal: https://lichtman.rc.fas.harvard.edu/octopus_connectomes/. **Verified—R.** Availability statement checked in [27]; portal returned a Neuroglancer redirect document, and segmentation metadata opened at https://storage.googleapis.com/octopus-connectomes/vertical_lobe/sgm/info. Metadata verifies public chunked segmentation, not a downloaded or analyzed synaptic graph.
