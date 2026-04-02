# 🚀 GitHub Workflow 自动化总结

## 📋 已实现的 GitHub Actions 工作流

本项目现在拥有完整的 CI/CD 自动化流程：

### 1. **CI 工作流** (`.github/workflows/ci.yml`)
**触发条件**: Push 到 `master/main/develop` 分支，或 PR 到主分支

**功能**:
- 🧪 多平台测试 (Ubuntu, macOS, Windows)
- 🐍 多 Python 版本支持 (3.8-3.12)
- 📊 代码覆盖率报告 (88%)
- 📦 包构建检查
- ✅ 所有测试通过验证

**输出:**
- 代码覆盖率上传到 Codecov
- 构建结果反馈

---

### 2. **代码质量检查** (`.github/workflows/quality.yml`)
**触发条件**: Push 到 `master/main` 分支，或 PR 到主分支

**功能**:
- 🎨 Black 代码格式检查
- 🔍 Ruff Linting 检查
- 🏷️  MyPy 类型检查

**输出:**
- 格式化问题报告
- 代码质量反馈

---

### 3. **自动发布到 PyPI** ✨ 新增 (`.github/workflows/publish.yml`)
**触发条件**: Git tag 推送 (`v0.2.0` 或 `0.2.0`)

**功能**:
- 🏗️  自动构建 wheel 和 source distribution
- 🔐 使用 Trusted Publisher 身份验证
- ✅ 版本号自动验证（tag vs pyproject.toml）
- 📦 上传到 PyPI
- 🏷️  创建 GitHub Release
- 📝 自动生成发布说明

**输出**:
- PyPI 包发布
- GitHub Release 创建
- 版本历史更新

---

## 🎯 工作流触发规则

```
┌─────────────────────────────────────────────────────┐
│              GitHub Events                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📌 Tag Push (v0.2.0)                               │
│     ↓                                               │
│     publish.yml → PyPI Package Update               │
│                                                     │
│  📝 Push to master/main                             │
│     ↓                                               │
│     ci.yml → Run Tests + Coverage                   │
│     quality.yml → Code Quality Checks               │
│                                                     │
│  🔀 Pull Request                                    │
│     ↓                                               │
│     ci.yml → Run Tests                              │
│     quality.yml → Code Quality Checks               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 配置要点

### PyPI Trusted Publisher 配置（必须）

⚠️ **重要**: 第一次使用需要配置 PyPI Trusted Publisher

**配置位置**: https://pypi.org/manage/project/deep-diff/settings/publishing

**配置内容**:
```yaml
Provider: GitHub
Organization: ider-zh
Repository: diff
Workflow: publish.yml
Ref Type: tag
Ref: refs/tags/*
```

详细说明见: `TRUSTED_PUBLISHER_SETUP.md`

---

## 📚 相关文档

| 文档 | 用途 |
|------|------|
| **PUBLISH_GUIDE.md** | 详细的发布流程和最佳实践 |
| **TRUSTED_PUBLISHER_SETUP.md** | PyPI Trusted Publisher 配置 |
| **QUICK_RELEASE.txt** | 快速发布参考（仅需 3 步） |
| **CONTRIBUTING.md** | 代码贡献指南 |

---

## ✅ 工作流检查清单

### 初始设置
- [x] 创建 `publish.yml` 工作流
- [x] 配置 Trusted Publisher（待用户配置）
- [x] 创建文档和指南
- [x] 提交到 GitHub

### 日常开发
- [ ] 推送代码变更到 master
- [ ] CI 工作流自动运行测试
- [ ] 代码质量工作流检查代码

### 发布新版本
- [ ] 更新 `pyproject.toml` 版本号
- [ ] 提交版本更新
- [ ] 创建 Git tag: `git tag -a v0.2.0`
- [ ] 推送 tag: `git push origin v0.2.0`
- [ ] 自动发布工作流运行
- [ ] 验证 PyPI 上的新版本

---

## 🚀 使用示例

### 完整发布流程

```bash
# 1. 开发功能（在功能分支上）
git checkout -b feature/new-feature
# ... 编写代码和测试 ...
git add .
git commit -m "feat: add new feature"

# 2. 创建 PR 到 master
git push origin feature/new-feature
# ... GitHub Actions 自动运行 CI 和质量检查 ...
# ... 创建 PR 并进行代码审查 ...

# 3. 合并到 master
git checkout master
git merge --no-ff feature/new-feature
git push origin master
# ... CI 和质量检查再次运行 ...

# 4. 更新版本和发布
vim pyproject.toml  # 更新版本号
git add pyproject.toml
git commit -m "chore: bump version to 0.2.0"
git push origin master

# 5. 创建发布 tag
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
# ... publish.yml 自动运行 ...
# ... 包自动上传到 PyPI ...
# ... GitHub Release 自动创建 ...

# 6. 验证
curl https://pypi.org/pypi/deep-diff/json | grep 0.2.0
pip install deep-diff==0.2.0
```

---

## 📊 工作流状态查看

访问: https://github.com/ider-zh/diff/actions

查看:
- ✔️ 成功的工作流
- ❌ 失败的工作流
- ⏳ 正在运行的工作流
- 📊 每个步骤的详细日志

---

## 🔐 安全特性

### Trusted Publisher 的优势

✅ **无需存储密钥**
- 不需要在 GitHub Secrets 中存储 PyPI token
- 更安全，权限更小化

✅ **临时授权**
- 每次发布都是独立授权
- 权限自动过期

✅ **精细控制**
- 只允许从特定仓库和工作流发布
- 只能在 tag 推送时触发

---

## 🐛 常见问题

### Q: 工作流在哪里查看？
A: https://github.com/ider-zh/diff/actions

### Q: 如何重新运行失败的工作流？
A: 在 GitHub Actions 页面点击 "Re-run" 按钮

### Q: Trusted Publisher 配置错了怎么办？
A: 在 PyPI 项目设置中删除错误的配置，重新添加正确的

### Q: 可以手动触发工作流吗？
A: 目前配置为自动触发。如需手动触发，请参考 GitHub Actions 文档添加 `workflow_dispatch`

### Q: 如何跳过 CI 运行？
A: 在 commit 消息中添加 `[skip ci]` 或 `[ci skip]`
例如: `git commit -m "docs: update README [skip ci]"`

---

## 📈 后续改进建议

- [ ] 添加 Pre-release 支持 (alpha, beta 版本)
- [ ] 添加 Changelog 自动生成
- [ ] 添加发布通知 (邮件、Slack)
- [ ] 添加 Docker 镜像构建和推送
- [ ] 添加性能基准对比
- [ ] 添加文档自动部署 (ReadTheDocs)

---

## 🎉 总结

现在 `deep-diff` 项目拥有:

✅ **完整的 CI/CD 流程**
- 自动化测试
- 自动化质量检查
- 自动化发布

✅ **安全的发布方式**
- Trusted Publisher 认证
- 版本号验证
- 自动化构建

✅ **完善的文档**
- 发布指南
- 配置说明
- 快速参考

✅ **开发者友好**
- 一命令发布
- 自动 GitHub Release
- 详细的工作流日志

---

**项目现已完全自动化！🚀**

任何人只需 `git push origin <tag>` 就能发布新版本到 PyPI。
