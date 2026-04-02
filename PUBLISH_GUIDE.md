# 📦 PyPI 发布指南

本文档说明如何使用自动化工作流将 `deep-diff` 发布到 PyPI。

## 🚀 自动发布流程

该项目配置了 GitHub Actions 工作流，在推送 Git tag 时自动发布到 PyPI。

### 工作流文件
- `.github/workflows/publish.yml` - 自动 PyPI 发布工作流

### 工作流功能
1. ✅ 监听 tag 推送事件
2. ✅ 验证版本号是否与 `pyproject.toml` 一致
3. ✅ 构建 wheel 和 source distribution
4. ✅ 上传到 PyPI
5. ✅ 创建 GitHub Release

## 📋 发布前的准备

### 1. 更新版本号

编辑 `pyproject.toml` 并更新版本号：

```toml
[project]
name = "deep-diff"
version = "0.2.0"  # 更新版本号
```

### 2. 更新 CHANGELOG（可选）

在 `pyproject.toml` 中的 Changelog 部分或在 README.md 中记录变更。

### 3. 提交代码

```bash
git add pyproject.toml
git commit -m "chore: bump version to 0.2.0"
git push origin master
```

### 4. 确保 CI 通过

等待 GitHub Actions CI 工作流完成，确保所有测试都通过。

## 🏷️ 发布新版本

### 方法 1: 使用命令行创建 tag（推荐）

```bash
# 创建带注释的 tag
git tag -a v0.2.0 -m "Release version 0.2.0"

# 推送 tag 到远程仓库
git push origin v0.2.0
```

### 方法 2: 使用 GitHub 网页界面

1. 访问 [GitHub Releases](https://github.com/ider-zh/diff/releases)
2. 点击 "Create a new release"
3. 填写 tag 名称（例如 `v0.2.0`）
4. 添加发布说明
5. 点击 "Publish release"

## 📊 发布流程示例

```bash
# 1. 更新版本
vim pyproject.toml  # 改成 0.2.0

# 2. 提交更新
git add pyproject.toml
git commit -m "chore: bump version to 0.2.0"

# 3. 创建 tag
git tag -a v0.2.0 -m "Release version 0.2.0"

# 4. 推送到 GitHub（自动触发发布工作流）
git push origin master
git push origin v0.2.0

# 5. 监控工作流进度
# - 访问 GitHub Actions 页面查看发布状态
# - 等待工作流完成

# 6. 验证发布
# - 访问 https://pypi.org/project/deep-diff/0.2.0/
# - 或运行: pip install deep-diff==0.2.0
```

## ⚙️ 工作流配置

### Tag 触发规则

工作流在以下情况下触发：
- `v*` - 所有以 `v` 开头的 tag（例如 `v0.2.0`）
- `[0-9]+.[0-9]+.[0-9]+` - 语义化版本（例如 `0.2.0`）

### 版本验证

工作流会验证 Git tag 版本与 `pyproject.toml` 中的版本是否一致：

```
Git tag: v0.2.0
pyproject.toml: version = "0.2.0"
✅ 匹配 → 继续发布
❌ 不匹配 → 发布失败
```

### 发布权限

本项目使用 **Trusted Publisher** 方式连接到 PyPI，无需存储密钥：

- ✨ 更安全：不需要在 GitHub Secrets 中存储 PyPI token
- ✨ 自动更新：PyPI 自动信任来自 GitHub 的发布
- ✨ 临时权限：每次发布都是独立授权

#### PyPI 配置要求

在 PyPI 项目设置中，需要配置 Trusted Publisher：

1. 访问 [PyPI deep-diff 设置](https://pypi.org/manage/project/deep-diff/settings/)
2. 进入 "Publishing" → "Trusted publishers"
3. 添加新的 Trusted Publisher：
   - **Workflow name**: `publish.yml`
   - **Environment name**: （留空）
   - **Owner**: `ider-zh`
   - **Repository name**: `diff`
   - **Ref type**: `tag`
   - **Ref**: `refs/tags/*`

## 🔍 监控发布进度

### GitHub Actions 页面

1. 访问项目的 [Actions 标签页](https://github.com/ider-zh/diff/actions)
2. 找到 "Publish to PyPI" 工作流
3. 点击最近的运行查看详细日志

### 工作流状态

工作流包含以下步骤：

```
1. Checkout code
   ↓
2. Set up Python
   ↓
3. Extract version from tag
   ↓
4. Verify version matches pyproject.toml
   ↓
5. Install dependencies
   ↓
6. Build distribution
   ↓
7. Publish to PyPI
   ↓
8. Create GitHub Release
   ↓
9. Summary
```

### 验证发布成功

发布完成后，验证：

```bash
# 方法 1: 访问 PyPI
curl -s https://pypi.org/pypi/deep-diff/json | python -m json.tool | grep -A 5 releases

# 方法 2: 尝试安装
pip install --upgrade deep-diff

# 方法 3: 检查版本
python -c "import deep_diff; print(deep_diff.__version__)"
```

## 🐛 故障排除

### 问题 1: 版本不匹配导致发布失败

**症状**: 工作流在 "Verify version" 步骤失败

**解决方案**:
```bash
# 确认 tag 和 pyproject.toml 版本一致
grep version pyproject.toml
git tag -l | tail -5
```

### 问题 2: Trusted Publisher 未配置

**症状**: 发布步骤返回认证错误

**解决方案**:
1. 在 PyPI 项目设置中添加 Trusted Publisher
2. 参考上方 "PyPI 配置要求" 部分

### 问题 3: Release 创建失败

**症状**: 工作流进行到 "Create GitHub Release" 时失败

**解决方案**:
- 这通常不影响 PyPI 发布
- 可以手动在 GitHub 上创建 Release

## 📝 更新日志管理

### 推荐的版本标签格式

```bash
git tag -a v0.2.0 -m "Release version 0.2.0

- Feature 1: 描述
- Feature 2: 描述
- Bug fix: 修复的问题"
```

### 发布说明模板

发布说明将自动在 GitHub Release 中创建，包含：
- 版本号
- PyPI 链接
- 安装说明

## 🎯 最佳实践

1. **语义化版本**: 遵循 [Semantic Versioning](https://semver.org/)
   - `MAJOR.MINOR.PATCH` (例如 `0.2.0`)

2. **提前验证**:
   ```bash
   # 创建 tag 后本地测试
   python -m build
   twine check dist/*
   ```

3. **一致性检查**:
   ```bash
   # 确保版本号一致
   grep "version" pyproject.toml
   grep "__version__" deep_diff/__init__.py  # 如有的话
   ```

4. **及时更新文档**:
   - 更新 README 中的安装版本
   - 更新 CHANGELOG 或发布说明

5. **测试发布**:
   ```bash
   # 使用 --dry-run 模式测试（如果支持）
   twine upload --repository testpypi dist/*
   ```

## 🔐 安全注意事项

### ✅ 不需要存储 PyPI Token

本项目使用 Trusted Publisher，**不需要** 在 GitHub Secrets 中存储任何密钥。

### ✅ 权限限制

工作流只能在以下条件下发布到 PyPI：
- 推送的是 git tag
- Tag 版本与 `pyproject.toml` 一致
- GitHub Actions 工作流来自官方仓库

## 📚 相关资源

- [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions for PyPI](https://github.com/pypa/gh-action-pypi-publish)
- [Semantic Versioning](https://semver.org/)
- [deep-diff on PyPI](https://pypi.org/project/deep-diff/)

## 💡 示例：完整发布流程

```bash
# 1. 在开发分支上完成功能
git checkout -b feature/new-feature
# ... 开发代码 ...
git add .
git commit -m "feat: add new feature"

# 2. 合并到主分支
git checkout master
git merge --no-ff feature/new-feature

# 3. 更新版本
vim pyproject.toml  # 0.1.0 → 0.2.0
git add pyproject.toml
git commit -m "chore: bump version to 0.2.0"

# 4. 创建 tag 并推送
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin master
git push origin v0.2.0

# 5. 监控发布（GitHub Actions 自动执行）
# 访问 https://github.com/ider-zh/diff/actions

# 6. 验证发布完成
pip install --upgrade deep-diff==0.2.0
python -c "import deep_diff; print('Successfully installed!')"
```

---

**需要帮助？** 创建一个 GitHub Issue 或查看项目的 CONTRIBUTING.md 文件。
