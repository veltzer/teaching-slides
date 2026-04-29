# Slides from Syllabi - Progress Tracker

Tracks the work of writing slide materials for syllabi in `../teaching-syllabi/` that don't yet have corresponding course material in `marp/courses/`.

- Syllabi: `../teaching-syllabi/syllabi/courses/<domain>/<course>.md`
- Materials: `marp/courses/<domain>/<course-with-dashes>/`

> **Note:** the per-domain checklists below were last bulk-reconciled some time ago and may undercount what already exists in `marp/courses/`. When picking a course, verify the directory doesn't already exist before starting. Update the checklist as you go.

## Status legend

- [ ] not started
- [~] in progress
- [x] done (all chapters written, builds clean)
- [-] decided not to write (out of scope, deprecated, etc.)

## Process per course

1. Read the syllabus to extract chapters and durations.
2. Create `marp/courses/<domain>/<course-with-dashes>/` directory.
3. Write `00_title.md` plus one `NN_<chapter>.md` per syllabus chapter.
4. Add `title.svg` and any per-chapter SVGs the material references.
5. Run `rsconstruct build --verbose -j10` and resolve all errors.
6. Mark the entry below `[x]` and commit (user commits, not me).

## Guidelines

- Target **~100 slides per training day** (roughly 12-13 slides per hour)
- A 2-day (16h) course should have ~200 slides
- A 1-day (8h) course should have ~100 slides
- Each course needs **SVG diagrams** (~1 per 8-10 text slides) in `svg/courses/<domain>/<course>/<chapter>/`
- Each course needs **code samples** (~1 per 10-15 slides) as inline fenced code blocks
- SVGs must use `var()` palette references, viewBox="0 0 1280 720", content ≤ y=630
- Default style follows existing courses (e.g. `marp/courses/ai/developing-using-ai/`): plain headings (no "Part N:"), `1. 1. 1.` ordered lists, dash bullets, project-root-relative SVG paths, palette-compliant SVGs.
- Skip syllabi that overlap heavily with already-written courses unless the syllabus introduces a meaningfully different angle/depth.
- Each course is roughly 8-15 chapters × ~700-1500 lines of well-written content + per-chapter SVGs. Writing one course end-to-end is several hours of focused work; this is a long-running task.

## Summary

| Domain | Existing | Missing | Total |
|--------|----------|---------|-------|
| ai | 3 | 13 | 16 |
| architecting | 8 | 18 | 26 |
| big_data | 0 | 16 | 16 |
| build_systems | 1 | 11 | 12 |
| cloud | 5 | 38 | 43 |
| containers | 0 | 4 | 4 |
| data_driven | 0 | 2 | 2 |
| data_engineering | 0 | 8 | 8 |
| data_science | 0 | 3 | 3 |
| databases | 1 | 26 | 27 |
| design_patterns | 0 | 2 | 2 |
| development_methodologies | 0 | 8 | 8 |
| devops | 4 | 33 | 37 |
| embedded | 1 | 10 | 11 |
| git | 1 | 4 | 5 |
| hardware | 0 | 5 | 5 |
| languages | 6 | 36 | 42 |
| machine_learning | 0 | 10 | 10 |
| networking | 1 | 15 | 16 |
| observability_and_monitoring | 0 | 14 | 14 |
| operating_systems | 0 | 5 | 5 |
| practices | 0 | 1 | 1 |
| principles | 0 | 2 | 2 |
| professional_skills | 0 | 5 | 5 |
| queues | 0 | 5 | 5 |
| real_time | 0 | 2 | 2 |
| security | 4 | 23 | 27 |
| testing | 0 | 20 | 20 |
| unity | 0 | 1 | 1 |
| wifi | 0 | 1 | 1 |
| **TOTAL** | **35** | **361** | **396** |

## ai (3/16)

- [x] advanced_ai_powered_development
- [ ] ai_agents_development
- [ ] ai_ethics_and_responsible_ai
- [ ] computer_vision_with_python
- [x] developing_using_ai
- [ ] explainable_ai
- [ ] federated_learning
- [x] generative_ai_applications
- [ ] llm_fine_tuning_and_prompt_engineering
- [ ] mlops
- [ ] nlp_with_python
- [ ] prompt_engineering
- [ ] rag_applications
- [ ] rag_deep_dive
- [ ] reinforcement_learning
- [ ] using_ai_when_developing_applications

## architecting (8/26)

- [x] api_design_best_practices — 12 chapters + title; 16h intermediate; 2 SVGs; build clean
- [ ] api_first_development
- [ ] api_gateway_patterns
- [x] architecting
- [ ] clean_and_hexagonal_architecture
- [ ] cloud_monolith_microservices_cloudnative_servicmesh
- [x] cqrs_and_event_sourcing — 9 chapters + title; 16h advanced; 33 SVGs; build clean
- [ ] data_mesh
- [ ] disaster_recovery
- [ ] distributed_systems_fundamentals
- [x] domain_driven_design — 7 chapters + title; 24h advanced; 1 SVG; build clean
- [ ] enterprise_architecture
- [ ] event_driven_architecture
- [ ] event_driven_architecture_with_kafka
- [ ] introduction_to_architecting
- [ ] large_scale_architecting
- [ ] legacy_modernization
- [ ] message_queues
- [x] microservices_architecture — 14 chapters + title; 16h intermediate; 1 SVG; build clean
- [x] modern_software_architecture
- [x] saga_pattern — 6 chapters + title; 8h advanced; 11 SVGs; build clean
- [ ] serverless_architecture
- [ ] site_reliability_engineering
- [ ] sre_practices
- [ ] system_design
- [x] twelve_factor_app — 15 chapters + title; 16h intermediate; 2 SVGs; build clean
- [ ] uml
- [ ] web_architecture_and_scaling

## big_data (0/16)

- [ ] beam
- [ ] dagster
- [ ] data_governance
- [ ] databricks
- [ ] delta_lake
- [ ] etl
- [ ] flink
- [ ] great_expectations
- [ ] hadoop_ecosystem
- [ ] iceberg
- [ ] prefect
- [ ] pyspark
- [ ] snowflake
- [ ] spark
- [ ] splunk
- [ ] superset

## build_systems (1/12)

- [ ] advanced_gradle
- [ ] bazel
- [ ] buck2
- [x] cmake
- [ ] gcc_in_depth
- [ ] gnu_make
- [ ] gradle
- [ ] maven
- [ ] meson
- [ ] msbuild
- [ ] nix
- [ ] scons

## cloud (5/43)

- [x] architecting_in_the_cloud
- [x] finops
- [x] introduction_to_cloud_computing
- [x] multi_cloud_strategy
- **aws (1/13)**
    - [x] introduction_to_aws
    - [ ] aws_architecting
    - [ ] aws_cdk
    - [ ] aws_containers
    - [ ] aws_data_analytics
    - [ ] aws_developer
    - [ ] aws_devops
    - [ ] aws_lambda_and_serverless
    - [ ] aws_migration
    - [ ] aws_networking
    - [ ] aws_security
    - [ ] aws_sysops
    - [ ] machine_learning_services_on_aws
- **azure (0/10)**
    - [ ] introduction_to_the_azure_cloud
    - [ ] aks
    - [ ] azure_administrator
    - [ ] azure_ai_services
    - [ ] azure_architect
    - [ ] azure_data_engineering
    - [ ] azure_devops
    - [ ] azure_networking
    - [ ] azure_security
    - [ ] serverless_on_azure
- **gcp (0/13)**
    - [ ] gcp_fundamentals
    - [ ] gcp_cloud_architect
    - [ ] gcp_cloud_engineer
    - [ ] gcp_data_engineering
    - [ ] gcp_devops_engineer
    - [ ] gcp_for_developers
    - [ ] gcp_ai_and_ml
    - [ ] gcp_migration
    - [ ] gcp_networking
    - [ ] gcp_security
    - [ ] gke
    - [ ] logging_monitoring_and_observability_in_the_google_cloud
    - [ ] serverless_on_gcp
- **cloud_foundry (0/1)**
    - [ ] introduction_to_cloud_foundry
- **openstack (0/1)**
    - [ ] openstack

## containers (0/4)

- [ ] docker_fundamentals
- [ ] kubernetes
- [ ] kubernetes_for_developers
- [ ] kubernetes_troubleshooting

## data_driven (0/2)

- [ ] data_analytics_for_managers
- [ ] data_driven_project_management

## data_engineering (0/8)

- [ ] airbyte
- [ ] apache_airflow
- [ ] apache_hudi
- [ ] apache_nifi
- [ ] data_lakehouse
- [ ] dbt
- [ ] temporal
- [ ] trino

## data_science (0/3)

- [ ] data_analyst_fundamentals
- [ ] data_science
- [ ] time_series_analysis

## databases (1/27)

- [ ] apache_druid
- [ ] arangodb
- [ ] cassandra
- [ ] clickhouse
- [ ] cockroachdb
- [ ] couchdb
- [ ] database_design
- [ ] database_migration_strategies
- [ ] duckdb
- [ ] dynamodb
- [ ] elasticsearch
- [ ] influxdb
- [ ] introduction_to_databases
- [ ] mariadb
- [ ] mongodb
- [ ] mysql
- [ ] neo4j
- [ ] oracle
- [ ] postgresql
- [x] redis
- [ ] scylladb
- [ ] solr
- [ ] sqlite
- [ ] supabase
- [ ] timescaledb
- [ ] vector_databases

## design_patterns (0/2)

- [ ] advanced_design_patterns
- [ ] design_patterns

## development_methodologies (0/8)

- [ ] code_review_best_practices
- [ ] development_methodologies
- [ ] incident_management
- [ ] modern_development
- [ ] scrum
- [ ] technical_writing
- [ ] terminal_productivity
- [ ] vim_and_neovim

## devops (4/37)

- [x] ansible
- [ ] apache_httpd
- [x] architectural_decisions_in_devops
- [ ] argo
- [ ] argocd
- [ ] argocd_and_gitops
- [ ] backstage
- [ ] chef
- [ ] consul
- [ ] crossplane
- [ ] dependency_management
- [ ] docker
- [ ] earthly
- [ ] fluxcd
- [ ] github
- [ ] github_actions
- [ ] gitlab
- [ ] helm
- [ ] introduction_to_devops
- [ ] istio
- [ ] jenkins
- [ ] kubernetes
- [ ] kustomize
- [ ] nexus
- [ ] nginx
- [ ] nomad
- [ ] packer
- [ ] platform_engineering
- [ ] podman
- [ ] pulumi
- [ ] puppet
- [ ] saltstack
- [ ] service_mesh
- [ ] tekton
- [x] terraform
- [ ] vault
- [x] welcome_to_the_world_of_devops

## embedded (1/11)

- [ ] ble_bluetooth_low_energy
- [ ] can_bus_and_automotive
- [ ] design_patterns_for_embedded_and_real_time_systems
- [x] effective_real_time_embedded_c_and_c++
- [ ] embedded_linux_networking
- [ ] embedded_programming_for_bare_metal
- [ ] fpga_programming
- [ ] lorawan_and_lpwan
- [ ] mqtt_and_iot_protocols
- [ ] rust_topics_for_embedded_systems_programming
- [ ] vxworks_and_non_secure_operating_systems

## git (1/5)

- [ ] advanced_git
- [x] git
- [ ] git_and_gerrit
- [ ] git_more_topics
- [ ] introduction_to_git

## hardware (0/5)

- [ ] arm_architecture
- [ ] basics_of_microcontroller_programming_and_testing
- [ ] multicore_and_multithreading_for_microcontrollers
- [ ] riscv_architecture
- [ ] working_with_hardware

## languages (6/42)

- [x] assembly
- [x] bash
- [x] c
- [x] c++
- [ ] clojure
- [ ] cobol
- [ ] crystal
- [ ] csharp
- [ ] dart
- [ ] dotnet
- [ ] elixir
- [ ] erlang
- [ ] fortran
- [ ] fsharp
- [ ] go
- [ ] groovy
- [ ] haskell
- [ ] introduction_to_programming_concepts
- [ ] java
- [ ] javascript
- [ ] julia
- [ ] kotlin
- [ ] lua
- [ ] mojo
- [ ] nim
- [ ] ocaml
- [ ] opencl
- [ ] perl
- [ ] php
- [ ] powershell
- [x] python
- [ ] r
- [ ] ruby
- [x] rust
- [ ] scala
- [ ] solidity
- [ ] sql
- [ ] swift
- [ ] tcl
- [ ] typescript
- [ ] webassembly
- [ ] zig

## machine_learning (0/10)

- [ ] deep_learning_fundamentals
- [ ] diffusion_models
- [ ] feature_engineering
- [ ] graph_neural_networks
- [ ] llm_application_development
- [ ] machine_learning
- [ ] ml1
- [ ] ml2
- [ ] mlflow
- [ ] nlp_with_transformers

## networking (1/16)

- [ ] dns_deep_dive
- [ ] graphql
- [ ] grpc
- [ ] http2_and_http3
- [ ] mobile_communication
- [ ] multi_cloud_networking
- [ ] network_security
- [ ] network_troubleshooting
- [x] networking_basics
- [ ] oauth2_and_oidc
- [ ] pki_and_certificates
- [ ] restful_apis
- [ ] software_defined_networking
- [ ] tcp_ip_deep_dive
- [ ] vpn_and_wireguard
- [ ] websocket_programming

## observability_and_monitoring (0/14)

- [ ] advanced_prometheus
- [ ] datadog
- [ ] dynatrace
- [ ] elk_deep_dive
- [ ] grafana_basics
- [ ] grafana_deep_dive
- [ ] jaeger
- [ ] loki
- [ ] nagios
- [ ] opentelemetry
- [ ] prometheus_and_grafana
- [ ] prometheus_deep_dive
- [ ] victoriametrics
- [ ] zabbix

## operating_systems (0/5)

- [ ] android
- [ ] freertos
- [ ] linux
- [ ] vxworks
- [ ] windows

## practices (0/1)

- [ ] agile_and_scrum

## principles (0/2)

- [ ] object_oriented_programming
- [ ] solid_clean_code

## professional_skills (0/5)

- [ ] devops_for_managers
- [ ] effective_presentations_for_engineers
- [ ] employability_and_career_skills
- [ ] interviewing_and_hiring_for_tech_leads
- [ ] linux_for_managers

## queues (0/5)

- [ ] activemq
- [ ] kafka
- [ ] nats
- [ ] pulsar
- [ ] rabbitmq

## real_time (0/2)

- [ ] real_time_design_patterns
- [ ] real_time_programming

## security (4/27)

- [ ] advanced_assembly_and_exploitation
- [ ] android_reverse_engineering
- [ ] android_security
- [ ] api_security
- [ ] application_security_owasp
- [ ] cloud_security
- [ ] container_and_kubernetes_security
- [ ] cryptography_fundamentals
- [ ] cyber_threats_and_attack_vectors
- [ ] devsecops
- [ ] gdpr_and_compliance
- [ ] identity_and_access_management
- [x] it_security_policies
- [ ] kubernetes_security
- [x] linux_forensics
- [ ] malware_analysis
- [ ] network_penetration_testing
- [ ] reverse_engineering_and_binary_analysis
- [ ] secure_sdlc
- [ ] soc_analyst_training
- [ ] supply_chain_security
- [ ] threat_modeling
- [x] web_application_hacking
- [ ] web_application_penetration_testing
- [ ] web_security
- [x] working_with_llms_securely
- [ ] zero_trust_security

## testing (0/20)

- [ ] advanced_playwright
- [ ] api_testing
- [ ] chaos_engineering
- [ ] contract_testing
- [ ] cypress
- [ ] gatling
- [ ] introduction_to_selenium
- [ ] jest
- [ ] junit5
- [ ] k6
- [ ] load_testing_deep_dive
- [ ] mutation_testing
- [ ] performance_testing
- [ ] playwright
- [ ] pytest_advanced
- [ ] robot_framework
- [ ] security_testing
- [ ] test_driven_development
- [ ] testcontainers
- [ ] testing_theory

## unity (0/1)

- [ ] introduction_to_game_development_with_unity

## wifi (0/1)

- [ ] wifi_protocols
