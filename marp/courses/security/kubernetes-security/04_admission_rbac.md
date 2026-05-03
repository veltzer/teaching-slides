---
tags:
  - security:kubernetes
  - concepts:rbac
  - concepts:admission-control
level: intermediate
category: security
audience:
  - audiences:devops

---
# Admission Controllers and RBAC

---
## What This Chapter Covers

- The Kubernetes API request flow
- RBAC: roles, bindings, service accounts
- Admission controllers: validating and mutating
- OPA Gatekeeper and Kyverno
- Common patterns and pitfalls

---
## API Request Flow

- Authentication — who is calling?
- Authorization (RBAC) — can they do this?
- Admission control — should this be allowed under policy?
- Validation — is the resource well-formed?
- Persistence in etcd
- Each step can reject the request

---
## Request Flow Visualized

![api_flow](svg/courses/security/kubernetes-security/04_admission_rbac/api_flow.svg)

---
## RBAC Basics

- Role-Based Access Control
- Built into the API server
- Resources: Roles, RoleBindings (namespace-scoped); ClusterRoles, ClusterRoleBindings (cluster-wide)
- Subjects: users, groups, service accounts
- Actions: verbs on resources

---
## Roles

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: prod
  name: pod-reader
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
```

---
## RoleBindings

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: prod
subjects:
  - kind: User
    name: alice
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

---
## ClusterRole and ClusterRoleBinding

- ClusterRole: cluster-wide permissions
- ClusterRoleBinding: applies a ClusterRole cluster-wide
- Or use ClusterRole with a RoleBinding for cluster-defined-role-namespace-scoped
- Useful for reusable roles

---
## Service Accounts

- Identities for pods
- Each namespace has a `default` service account
- Mount tokens into pods for API access
- Default token mounts can be disabled
- The principal for pod-initiated API calls

---
## Default Service Account Risks

- Default SA has no permissions out of the box (good)
- But pods get its token mounted automatically
- A compromised pod can call the API as default SA
- automountServiceAccountToken: false to disable
- Set explicitly per pod when API access is needed

---
## Least Privilege Principle

- Grant only what each subject actually needs
- Avoid cluster-admin everywhere
- Specific roles per workload
- Audit and remove unused permissions
- Reduces blast radius of compromise

---
## Verb Resource Scope

![least_privilege_rbac](svg/courses/security/kubernetes-security/04_admission_rbac/least_privilege_rbac.svg)

---
## RBAC Anti-Patterns

- Wildcard verbs (`*`)
- Wildcard resources (`*`)
- ClusterRoleBinding to system:masters
- Long-lived bound users
- Granting cluster-admin "for convenience"

---
## Auditing RBAC

- `kubectl auth can-i` — check permissions
- `rbac-tool` — analyze and visualize
- `rbac-lookup` — see what subjects have what
- `kubeaudit` — find common misconfigurations
- Run periodically; document findings

---
## Admission Controllers

- Plugins that run after authn/authz
- Validating: accept or reject
- Mutating: change the resource (e.g., add sidecars)
- Some are built-in; webhooks are dynamic
- Where most policy enforcement happens today

---
## Built-in Admission Controllers

- NodeRestriction — kubelets can only modify their own node/pods
- PodSecurity — enforces PSS labels
- ResourceQuota — enforces namespace quotas
- LimitRanger — applies default limits
- Many more; some defaulted on per cluster

---
## Admission Controller Kinds

![admission_kinds](svg/courses/security/kubernetes-security/04_admission_rbac/admission_kinds.svg)

---
## Validating Admission Webhooks

- Custom logic via HTTPS endpoint
- Receives the resource being created/updated
- Returns allow/deny
- Can implement any policy
- The basis for OPA Gatekeeper, Kyverno, etc

---
## Mutating Admission Webhooks

- Can modify resources before persisting
- Add sidecars, set defaults, inject labels
- Common: service mesh sidecar injection
- Order matters; mutating runs before validating
- Powerful but risky

---
## OPA Gatekeeper

- Open Policy Agent integration with Kubernetes
- Rego policy language
- Constraints: instantiate templates with parameters
- Policies as code; version-controlled
- Strong fit for compliance automation

---
## Gatekeeper Example

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: ns-must-have-owner
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Namespace"]
  parameters:
    labels: ["owner"]
```

---
## Kyverno

- Kubernetes-native policy engine
- YAML-based policies (no Rego)
- Validate, mutate, generate
- Lower learning curve than Gatekeeper
- Increasingly popular

---
## Kyverno Example

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-non-root
spec:
  validationFailureAction: Enforce
  rules:
    - name: check-non-root
      match:
        any:
          - resources:
              kinds: [Pod]
      validate:
        message: "Containers must run as non-root"
        pattern:
          spec:
            securityContext:
              runAsNonRoot: true
```

---
## OPA vs Kyverno

- Gatekeeper — Rego, complex but powerful
- Kyverno — YAML, faster onboarding
- Both production-ready
- Pick based on team familiarity
- Some teams use both for different policies

---
## Common Policies

- Disallow privileged containers
- Require resource limits
- Require labels for ownership
- Disallow latest image tags
- Restrict image registries
- Each is a one-policy lift

---
## Policy Coverage Strategy

- Start with PSS at namespace level
- Add policies for things PSS doesn't cover
- Test in audit mode first
- Communicate policies to teams
- Iterate based on real workloads

---
## RBAC + Admission Together

- RBAC controls *who* can do what
- Admission controls *what* gets accepted
- Different layers; both needed
- A user with permission to create pods + Pod Security admission = pods follow policy
- Defense in depth

---
## Kubectl Plugins for Audit

- kubectl-who-can — find who can do an action
- kubectl-rolesum — summarize a role
- kubectl-access-matrix — full permission map
- Useful for periodic audits
- Build into onboarding for new admins

---
## Token Best Practices

- Short-lived tokens (use BoundServiceAccountTokenVolume)
- Auto-rotation enabled
- Disable default token mount when not needed
- Rotate certs and tokens regularly
- Audit log every token issuance

---
## Common Pitfalls

- Granting cluster-admin to "make it work"
- Forgetting service account permissions when scoping users
- Mutating webhooks that fail open
- Policy engines without monitoring
- Untested policies that break workloads

---
## Best Practices

- Least-privilege RBAC; audit periodically
- Default-deny via admission policies
- Use Kyverno or Gatekeeper for org policies
- Disable default service account token mounting
- Monitor admission webhook failures

---
## Summary

- RBAC: who can call the API and do what
- Admission: what the cluster accepts under policy
- Both layered for defense in depth
- Kyverno (YAML) and Gatekeeper (Rego) as policy engines
- Least privilege, default deny, audit relentlessly
