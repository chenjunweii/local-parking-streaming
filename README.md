
```shell
python setup.py build_ext
```

```shell
cd C:\Users\sapph\AppData\Local\Programs\Python\Python311\Scripts
```


```shell
pyinstaller --noconfirm --onefile --console --icon "C:/Project/local-parking-streaming/assets/streaming.ico" --upx-dir "C:/Project/upx-4.1.0-win64" --add-binary "C:/Project/local-parking-streaming/build/lib.win-amd64-cpython-311/config.cp311-win_amd64.pyd;." --add-binary "C:/Project/local-parking-streaming/build/lib.win-amd64-cpython-311/service.cp311-win_amd64.pyd;."  "C:/Project/local-parking-streaming/app.py"
```
