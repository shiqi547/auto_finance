配置要求
一.Gmail API
二.Google Cloud Service Account的电子邮件地址
三.服务器上配置框架，我使用的是Django：以下都是建立在Django下：
   ---代码放入一个Django app的views.py文件
   ---在urls.py中为该视图函数添加一个URL路径，urlpatterns = [path('myapp/', include('myapp.urls')),]
   ---setting.py加入字段：ALLOWED_HOSTS = ['服务器公有IP地址', '127.0.0.1', 'localhost', '*']
四.服务器上安装必要的库：pip install django web3 gspread oauth2client requests
五.使用固定的google excel框架
   ---按照https://docs.google.com/spreadsheets/d/1cE5C6b33FsRoXyGsPan1l2DSIrhHW0JplCsZ5CuRFyU/edit#gid=137100285
   ---google excel的sheet2中，要在第一列加一个结束符，行数大于view.py332行的数据即可，可仿照上一行中excel中的72行
六.打开对应的URl即可执行

-----Google Cloud Service Account的电子邮件地址-----
1.访问 Google Cloud Console.https://console.cloud.google.com/iam-admin/iam
选择你的项目:

2.在页面顶部的下拉列表中，选择你的项目（例如caiwu-393309）。
导航到IAM & Admin:

3.在左侧的导航面板中，点击 "IAM & Admin"，然后点击 "Service Accounts"。
查找服务账号:

4.在"Service Accounts"页面中，你应该能看到一个或多个服务账户。没有则创建
复制电子邮件地址:caiwu-719@caiwu-393309.iam.gserviceaccount.com类似

5.将此电子邮件地址添加到对应的Google excel的访问权限中

-----Gmail API-----
1. **Google Cloud Console**:
   - 访问 [Google Cloud Console](https://console.cloud.google.com/).

2. **创建或选择一个项目**:
   - 在页面顶部的下拉列表中，选择一个现有项目或创建一个新项目。

3. **启用Gmail API**:
   - 在导航菜单中点击 "API & Services"，然后点击 "Library".
   - 在搜索框中输入 "Gmail"，并选择"Gmail API"。
   - 点击 "Enable" 按钮来启用Gmail API为你的项目。

4. **设置OAuth 2.0客户端ID**:
   - 返回导航菜单，点击 "API & Services"，然后点击 "Credentials".
   - 点击 "Create Credentials" 按钮并选择 "OAuth 2.0 Client ID".
   - 选择 "Desktop App" (如果你正在为一个桌面应用创建凭据)。
   - 输入名称，然后点击 "Create"。
   - 点击 "OK" 关闭弹出窗口。
   - 在列表中，你应该能看到你新创建的OAuth 2.0客户端ID。点击下载按钮(形如一个下载箭头)来下载你的凭据。

5. **下载的凭据**:
   - 你应该现在有一个名为 `credentials.json` 的文件，其中包含你需要进行身份验证和使用Gmail API的凭据。