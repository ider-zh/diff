# 🔐 PyPI Trusted Publisher 配置指南

本文档说明如何配置 **PyPI Trusted Publisher** 使 GitHub Actions 能够自动向 PyPI 发布包。

## 🎯 概述

**Trusted Publisher** 是 PyPI 提供的一种安全的发布方式，它：
- ✅ 无需在 GitHub 存储 PyPI API token
- ✅ 使用 OIDC（OpenID Connect）进行身份验证
- ✅ 权限作用域限制到特定的 GitHub 仓库和工作流
- ✅ 每次发布都是独立授权，更加安全

## 📋 前置条件

1. **PyPI 账户**: 拥有 `deep-diff` 项目的管理员权限
2. **GitHub 仓库**: `ider-zh/diff`
3. **Publish 工作流**: `.github/workflows/publish.yml` 已配置

## 🔧 配置步骤

### 第 1 步: 访问 PyPI 项目设置

1. 访问 [PyPI deep-diff 项目页面](https://pypi.org/project/deep-diff/)
2. 点击右侧的 "Manage" 或进入项目设置
3. 选择 **"Publishing"** 标签页

### 第 2 步: 配置 Trusted Publisher

#### 添加 Trusted Publisher

1. 在 **"Trusted publishers"** 部分找到 **"Add a new trusted publisher"** 按钮
2. 选择以下配置：

```yaml
Provider: GitHub
Project: ider-zh/diff Workflow: publish.yml
Environment: (留空 - 生产环境)
```

3. 具体字段填写：

| 字段 | 值 |
|------|-----|
| **Provider** | GitHub |
| **GitHub Organization or User** | `ider-zh` |
| **GitHub Repository Name** | `diff` |
| **GitHub Workflow Filename** | `publish.yml` |
| **GitHub Environment Name** | （留空） |
| **Ref Type** | `tag` |
| **Ref** | `refs/tags/*` |

4. 点击 **"Add trusted publisher"** 确认

### 第 3 步: 验证配置

配置完成后，你应该看到：

```
Trusted Publishers
✅ GitHub (ider-zh/diff, publish.yml)
   Ref: tags/*
   Environment: (not set)
```

## 🧪 测试工作流

### 创建测试版本

```bash
# 1. 更新版本号到 0.1.1（测试版本）
vim pyproject.toml
# version = "0.1.1"

# 2. 提交更新
git add pyproject.toml
git commit -m "chore: bump version to 0.1.1 (test)"

# 3. 创建测试 tag
git tag -a v0.1.1 -m "Test release v0.1.1"

# 4. 推送 tag（这将触发工作流）
git push origin v0.1.1
```

### 监控工作流

1. 访问 [GitHub Actions](https://github.com/ider-zh/diff/actions)
2. 找到 "Publish to PyPI" 工作流
3. 查看最新的运行日志

### 预期结果

- ✅ 所有步骤应该通过
- ✅ 包已上传到 PyPI
- ✅ GitHub Release 已创建

## 🔍 故障排除

### 问题 1: 工作流在 "Publish" 步骤失败

**错误消息**: `Error: Publish failed` 或 `401 Unauthorized`

**原因**: Trusted Publisher 配置不正确

**解决方案**:
1. 确认 PyPI 项目设置中已添加 Trusted Publisher
2. 检查 organization/repository/workflow 名称是否完全匹配
3. 确保 tag 名称符合格式（`v*` 或 `[0-9]+.[0-9]+.[0-9]+`）

### 问题 2: 工作流在版本验证失败

**错误消息**: `Version mismatch!`

**原因**: Git tag 版本与 pyproject.toml 版本不一致

**解决方案**:
```bash
# 查看当前版本
grep "version" pyproject.toml

# 创建匹配的 tag
git tag -a v0.1.0 -m "Release 0.1.0"  # 如果 pyproject.toml 中是 0.1.0
```

### 问题 3: GitHub Release 创建失败

**原因**: 工作流使用的 API 权限不足

**解决方案**:
- 这不影响 PyPI 发布
- 可以手动在 GitHub 上创建 Release
- 下次推送 tag 时工作流会重试

## 📊 工作流流程图

```
Git Tag Push (v0.2.0)
        ↓
   GitHub Actions
        ↓
┌─────────────────────────────┐
│ 1. Checkout code            │
│ 2. Setup Python 3.11        │
│ 3. Extract version info     │
│ 4. Verify version match     │
│ 5. Build package            │
│ 6. Publish to PyPI          │  ← Trusted Publisher
│ 7. Create GitHub Release    │
└─────────────────────────────┘
        ↓
   ✅ Success
        ↓
┌─────────────────────────────┐
│ PyPI package updated        │
│ GitHub Release created      │
│ notify maintainers          │
└─────────────────────────────┘
```

## 🎯 常见场景

### 场景 1: 正常发布新版本

```bash
# 更新代码和文档
git add .
git commit -m "feat: add new features"

# 更新版本
sed -i 's/version = "0.1.0"/version = "0.2.0"/' pyproject.toml
git add pyproject.toml
git commit -m "chore: bump version to 0.2.0"

# 推送代码
git push origin master

# 创建并推送 tag（自动发布）
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
```

### 场景 2: 修复发布中的错误

```bash
# 修复问题
git fix-tag-issue
git commit -m "fix: resolve issue in v0.2.0"

# 创建新版本
sed -i 's/version = "0.2.0"/version = "0.2.1"/' pyproject.toml
git commit -am "chore: bump to 0.2.1"

# 发布新版本
git tag -a v0.2.1 -m "Release v0.2.1 (hotfix)"
git push origin master v0.2.1
```

### 场景 3: 删除错误的 tag

```bash
# 删除本地 tag
git tag -d v0.2.0

# 删除远程 tag
git push origin --delete v0.2.0

# 创建正确的 tag
git tag -a v0.2.0 -m "Release v0.2.0 (corrected)"
git push origin v0.2.0
```

## ⚙️ Trusted Publisher 权限

你配置的 Trusted Publisher 允许：

✅ **允许的操作**:
- 从 `refs/tags/*` 推送发布
- 发布到 PyPI `deep-diff` 项目
- 来自 `ider-zh/diff` 仓库

❌ **不允许的操作**:
- 从非 tag 推送发布（例如从分支）
- 发布到其他 PyPI 项目
- 来自其他仓库的发布

## 🔐 安全最佳实践

1. **分支保护**: 只允许在 `master` 分支上创建 tag
   ```
   Repository Settings → Branches → Require status checks to pass before merging
   ```

2. **Code Review**: 所有代码变更都需要 PR 审查

3. **CI/CD 检查**: 确保 CI 通过才能创建 tag
   ```bash
   # 在创建 tag 前检查 CI 状态
   gh run list --status success --limit 1
   ```

4. **仓库频密**: 定期检查谁有发布权限
   ```bash
   # 查看 PyPI 项目的协作者
   # 在 PyPI 项目设置中的 "Collaborators" 标签页
   ```

## 📚 参考资源

- [PyPI Trusted Publishers 文档](https://docs.pypi.org/trusted-publishers/)
- [GitHub OIDC 文档](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)
- [PEP 698 - Trusted Publishers](https://peps.python.org/pep-0698/)

## 💬 常见问题

**Q: 为什么要使用 Trusted Publisher？**
A: 它比存储 API token 更安全，自动管理权限，且 token 不会过期。

**Q: 如果配置出错怎么办？**
A: 可以随时删除错误的配置并重新添加。删除不会影响已发布的包。

**Q: 可以同时用 Token 和 Trusted Publisher 吗？**
A: 可以，但推荐只用 Trusted Publisher 以获得最佳安全性。

**Q: Trusted Publisher 有哪些限制？**
A: 只能在推送 tag 时触发。分支推送将使用其他认证方式（如 token）。

---

**配置完成后**，你就可以通过简单的 `git push origin <tag>` 来自动发布新版本到 PyPI！🚀
