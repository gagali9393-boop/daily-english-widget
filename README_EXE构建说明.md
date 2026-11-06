# Daily English 独立 EXE 云端构建包

本包使用 GitHub Actions 的 Windows 构建环境生成真正的 Windows x64 单文件 EXE。
日常运行 EXE 的电脑不需要安装 Python，也不需要携带 quotes.json。

## 获取 EXE（推荐方式）

1. 登录 GitHub，创建一个新的空仓库，例如 `daily-english-widget`。
2. 将本压缩包解压，把里面的全部文件（包括 `.github` 隐藏文件夹）上传到仓库根目录。
   - 可以在 GitHub 仓库页面选择 **Add file → Upload files**。
   - 确认 `.github/workflows/build-windows.yml` 也已上传。
3. 打开仓库顶部的 **Actions** 页面。
4. 如果出现提示，点击 **I understand my workflows, go ahead and enable them**。
5. 选择 **Build DailyEnglish Windows EXE** 工作流，点击 **Run workflow**。
6. 等待任务显示绿色成功状态。
7. 打开本次运行记录，在页面底部 **Artifacts** 区域下载 `DailyEnglish-Windows-x64`。
8. 解压后得到 `DailyEnglish.exe`，复制到 Windows 电脑，双击运行即可。

## 重要说明

- 这是 Windows x64 的单文件打包配置，`quotes.json` 会被一起嵌入 EXE。
- 构建过程在 GitHub 的 Windows runner 上完成；运行 EXE 的电脑不需要 Python。
- 当前工作流使用 GitHub 官方 Actions：checkout、setup-python、upload-artifact。
- 本交付物是构建包，不是已经编译好的 EXE。当前执行环境为 Linux，不能在这里直接产出并验证 Windows 可执行文件。
- GitHub 下载的 artifact 是一个压缩包，解压后才是 `DailyEnglish.exe`。
- 如果 Windows SmartScreen 弹出未知发布者提示，这是因为程序没有代码签名；只从你自己的构建仓库下载并确认来源。
