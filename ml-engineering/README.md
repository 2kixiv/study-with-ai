# ML Engineering 문제 풀이 트랙

ML Engineering을 하나의 짧은 모델링 과정으로 다루지 않고 네 영역으로
분리합니다. 데이터가 만들어지는 과정, 전통 머신러닝, 딥러닝, 실제 학습·추론
시스템을 각각 기초부터 학습한 뒤 종합 프로젝트에서 연결합니다.

```text
data-engineering ─┐
                  ├─> ml-systems ─> MLOps
machine-learning ─┤
                  │
deep-learning ────┘
```

각 하위 트랙은 자체 번호를 사용합니다. 로드맵은 학습 방향이며 실제 과제
폴더는 한 번에 하나씩 추가합니다.

## 1. Data Engineering

경로: `ml-engineering/data-engineering`

모델 학습에 사용할 데이터를 안전하고 재현 가능하게 수집·검증·변환·저장하는
과정을 학습합니다. 범용 데이터 엔지니어링 원리와 ML 데이터 특성을 함께
다룹니다.

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 01 | 데이터 검증과 분할 | schema, 결측·범위, 누수, stratified split |
| 02 | CSV·JSON 수집 | parsing, encoding, malformed row, schema 변환 |
| 03 | SQL 기초 | SELECT, JOIN, GROUP BY, window function |
| 04 | ETL 파이프라인 | extract/transform/load, 단계 분리, 실패 처리 |
| 05 | 멱등성과 증분 적재 | upsert, checkpoint, 재실행, 중복 방지 |
| 06 | 데이터 품질 테스트 | completeness, uniqueness, validity, freshness |
| 07 | Parquet과 열 지향 저장 | schema, compression, predicate pushdown |
| 08 | 파티셔닝 | partition key, small file, pruning |
| 09 | 시점 데이터와 누수 | event time, point-in-time join, label leakage |
| 10 | 데이터셋 버전과 계보 | snapshot, hash, metadata, lineage |
| 11 | 워크플로 오케스트레이션 | DAG, dependency, retry, backfill |
| 12 | Spark DataFrame 기초 | lazy evaluation, transformation, action |
| 13 | Spark join과 shuffle | partition, skew, broadcast join |
| 14 | 분산 집계 최적화 | shuffle 감소, caching, execution plan |
| 15 | 메시지 스트리밍 | Kafka topic, partition, offset, consumer group |
| 16 | 스트림 처리 | event time, watermark, window, late event |
| 17 | Lakehouse 기초 | table format, transaction, schema evolution |
| 18 | 데이터 파이프라인 프로젝트 | 수집·검증·증분 처리·품질·계보 통합 |

## 2. Machine Learning

경로: `ml-engineering/machine-learning`

알고리즘을 NumPy로 직접 구현해 원리를 확인한 뒤 scikit-learn으로 같은 문제를
해결합니다. 수식 암기보다 입력, 손실 함수, 최적화, 일반화, 평가의 연결을
이해하는 것이 목표입니다.

### 수학과 학습 기초

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 01 | NumPy와 벡터 연산 | shape, broadcasting, vectorization |
| 02 | 선형대수 기초 | vector, matrix, dot product, inverse, eigenvalue |
| 03 | 확률과 통계 | 분포, 기대값, 분산, sampling, confidence interval |
| 04 | 미분과 경사하강법 | derivative, gradient, learning rate, convergence |
| 05 | 데이터 분할과 기준선 | train/validation/test, dummy baseline, leakage |

### 지도학습: 회귀와 분류

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 06 | 단순 선형 회귀 | 최소제곱, MSE, 해석 |
| 07 | 다중 선형 회귀 | 행렬 해법, 다중공선성 |
| 08 | 경사하강 선형 회귀 | batch/SGD, scaling, 수렴 진단 |
| 09 | 회귀 규제 | Ridge, Lasso, bias-variance |
| 10 | 이진 로지스틱 회귀 | sigmoid, log loss, decision boundary |
| 11 | 다중 분류 | softmax, cross entropy, one-vs-rest |
| 12 | 분류 평가 | confusion matrix, precision/recall, ROC/PR |
| 13 | 임계값과 확률 보정 | threshold, calibration, 비용 기반 판단 |
| 14 | k-최근접 이웃 | distance, scaling, curse of dimensionality |
| 15 | Naive Bayes | 조건부 확률, text classification |
| 16 | 결정 트리 | impurity, split, pruning, overfitting |
| 17 | Random Forest | bagging, feature sampling, OOB |
| 18 | Gradient Boosting | residual fitting, learning rate, boosting |
| 19 | SVM | margin, kernel, regularization |

### 비지도학습과 실전 모델링

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 20 | k-means 군집화 | centroid, initialization, silhouette |
| 21 | 계층 군집과 DBSCAN | density, dendrogram, noise |
| 22 | PCA 차원 축소 | covariance, eigenvector, explained variance |
| 23 | 이상 탐지 | isolation, reconstruction, threshold |
| 24 | 전처리 Pipeline | imputation, encoding, scaling, ColumnTransformer |
| 25 | 교차 검증 | k-fold, stratified/group/time-series split |
| 26 | 하이퍼파라미터 탐색 | grid/random/Bayesian search, nested CV |
| 27 | 불균형 데이터 | class weight, resampling, metric 선택 |
| 28 | 모델 해석 | coefficient, permutation, PDP, SHAP 개념 |
| 29 | 시계열 예측 기초 | lag, seasonality, walk-forward validation |
| 30 | 전통 ML 종합 프로젝트 | 문제 정의부터 모델 카드까지 |

## 3. Deep Learning

경로: `ml-engineering/deep-learning`

작은 수치 구현으로 역전파를 이해한 후 PyTorch를 사용합니다. 선형 회귀와
이진 분류부터 CNN, RNN, Attention, Transformer까지 모델 구조와 학습 과정을
세분화해 진행합니다.

### 신경망 기초

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 01 | Tensor 기초 | shape, dtype, device, broadcasting |
| 02 | 수치 미분과 계산 그래프 | chain rule, computational graph |
| 03 | Autograd | requires_grad, backward, gradient 누적 |
| 04 | 선형 회귀 | `nn.Module`, MSE, optimizer, 학습 루프 |
| 05 | 이진 분류 | logit, sigmoid, BCEWithLogitsLoss |
| 06 | 다중 분류 | softmax, CrossEntropyLoss, class index |
| 07 | 다층 퍼셉트론 | hidden layer, representation, nonlinearity |
| 08 | 활성화와 초기화 | ReLU/GELU, Xavier/He, gradient 흐름 |
| 09 | 최적화 알고리즘 | SGD, momentum, Adam, scheduler |
| 10 | 일반화 | dropout, weight decay, early stopping |
| 11 | Dataset과 DataLoader | batch, shuffle, custom dataset, worker |
| 12 | 견고한 학습 루프 | validation, checkpoint, resume, seed |

### 컴퓨터 비전

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 13 | CNN 기초 | convolution, kernel, padding, stride, pooling |
| 14 | 이미지 분류 CNN | channel, feature map, classifier head |
| 15 | 데이터 증강 | train/test transform, augmentation 판단 |
| 16 | Batch Normalization | train/eval mode, running statistics |
| 17 | Residual Network | skip connection, 깊은 네트워크 |
| 18 | 전이 학습 | pretrained model, freezing, fine-tuning |
| 19 | 객체 탐지 입문 | bounding box, IoU, NMS, mAP |
| 20 | 이미지 분할 입문 | pixel classification, U-Net, Dice/IoU |

### 시퀀스와 자연어 처리

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 21 | 시퀀스 데이터 | padding, masking, variable length |
| 22 | Vanilla RNN | hidden state, BPTT, gradient 문제 |
| 23 | LSTM | gate, cell state, 장기 의존성 |
| 24 | GRU | 구조 비교, 시계열·텍스트 분류 |
| 25 | Seq2Seq | encoder/decoder, teacher forcing |
| 26 | Attention | query/key/value 이전의 attention 원리 |
| 27 | Token과 Embedding | vocabulary, subword, embedding layer |
| 28 | Transformer 구성 요소 | self-attention, multi-head, positional encoding |
| 29 | Transformer 직접 구현 | encoder block, mask, residual, normalization |
| 30 | 사전학습 모델 fine-tuning | tokenizer, classification head, scheduler |
| 31 | 언어 모델 기초 | causal mask, next-token objective, perplexity |
| 32 | 임베딩과 검색 | semantic embedding, similarity, retrieval |

### 생성 모델과 확장

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 33 | Autoencoder | latent representation, reconstruction |
| 34 | Variational Autoencoder | probabilistic latent, KL divergence |
| 35 | GAN 기초 | generator/discriminator, adversarial loss |
| 36 | Diffusion 기초 | noise schedule, denoising objective |
| 37 | 혼합 정밀도 | FP16/BF16, gradient scaling |
| 38 | 다중 GPU 학습 | data parallel, distributed sampler |
| 39 | 모델 압축 | quantization, pruning, distillation |
| 40 | 딥러닝 종합 프로젝트 | 데이터·학습·평가·추론·모델 카드 |

## 4. ML Systems

경로: `ml-engineering/ml-systems`

모델 자체보다 모델을 안정적으로 학습하고 빠르게 추론하는 소프트웨어 시스템에
집중합니다. MLOps가 수명주기 자동화와 운영 정책을 다룬다면, 이 영역은 학습·
추론 코드의 구조와 실행 성능을 다룹니다.

| 번호 | 과제 | 핵심 내용 |
|---|---|---|
| 01 | 재현 가능한 프로젝트 구조 | config, seed, dependency, entrypoint |
| 02 | 특성 파이프라인 | fit/transform, train-serving consistency |
| 03 | 학습 파이프라인 | 단계 경계, artifact, 오류 전파 |
| 04 | 모델 직렬화 | format, compatibility, 안전한 loading |
| 05 | 모델 입출력 계약 | schema, shape, dtype, signature |
| 06 | 배치 추론 | chunk, checkpoint, partial failure, idempotency |
| 07 | 온라인 추론 API | validation, latency, concurrency, timeout |
| 08 | 동적 배칭 | queue, batch window, throughput-latency tradeoff |
| 09 | 모델 서버 프로세스 | preload, worker, memory sharing, graceful shutdown |
| 10 | CPU 추론 최적화 | vectorization, thread, ONNX, profiling |
| 11 | GPU 추론 최적화 | transfer, batching, memory, utilization |
| 12 | 대규모 학습 입력 | sharding, prefetch, caching, bottleneck |
| 13 | 분산 학습 시스템 | worker, collective, checkpoint, failure |
| 14 | Feature Store 개념 | offline/online, freshness, point-in-time join |
| 15 | 검색·추천 시스템 | candidate, ranking, ANN index |
| 16 | RAG 파이프라인 | chunk, embedding, retrieval, evaluation |
| 17 | 모델 테스트 | invariance, metamorphic, regression, golden set |
| 18 | 성능·비용 벤치마크 | throughput, p95, memory, cost per prediction |
| 19 | 장애 허용 추론 | fallback, circuit breaker, degraded mode |
| 20 | ML 시스템 종합 프로젝트 | 학습부터 확장 가능한 서빙까지 |

## 트랙 간 권장 순서

- Data Engineering 01~06 → Machine Learning 01~13
- Machine Learning의 선형 회귀·분류 이후 Deep Learning 01 시작
- Deep Learning 12 또는 전통 ML 프로젝트 이후 ML Systems 시작
- 재현 가능한 학습 코드가 완성되면 MLOps 01 시작
- 이후에는 프로젝트에 필요한 영역을 교차해 진행

## 공통 원칙

- 데이터 계약과 모델 입출력을 코드와 테스트로 명시합니다.
- 식별자, 미래 정보, 정답에서 파생된 특성의 누수를 막습니다.
- 학습·검증·테스트 데이터의 역할을 구분합니다.
- 먼저 단순한 기준선을 만들고 복잡한 모델이 실제로 개선하는지 검증합니다.
- 정확도뿐 아니라 재현성, 지연 시간, 메모리, 실패 방식도 측정합니다.
- 과제 폴더끼리 코드를 직접 import하지 않습니다.

