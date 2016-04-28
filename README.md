# PHOSCC

PHOS.CC 主站程序，使用 Flask 框架，部署在 LeanCloud 云引擎上。

## 本地运行

参照 [LeanCloud云引擎](https://leancloud.cn/docs/leanengine_guide-python.html)

安装 LeanCloud 命令行工具

```
npm install -g avoscloud-code
```

绑定程序到 Leancloud

```
leancloud add <APP-NAME> <APP-ID>
```

安装依赖
```
sudo pip install -Ur requirements.txt
```

启动应用
```
leancloud up
```

应用即可启动运行：http://localhost:3000

## 部署到线上

部署到预备环境

```
leancloud deploy
```

部署到生产环境

```
leancloud publish
```



