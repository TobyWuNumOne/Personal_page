# Personal Page

個人網站專案，包含前端應用與後台內容管理系統。

## 專案架構

### 📱 frontend/
**Vercel 部署的前端應用**

- **技術棧：** Vue.js + Vite + Tailwind CSS
- **部署平台：** Vercel
- **網域：** 主網域（待設定）
- **說明：** 個人網站的前端介面，包含首頁、作品集、部落格等頁面

**部署步驟：**
1. 推送程式碼到 GitHub
2. 在 Vercel 連接 GitHub 儲存庫
3. 設定建置指令：`cd frontend && npm run build`
4. 設定輸出目錄：`frontend/dist`
5. 配置自訂網域（如需要）

### 🗄️ cms/
**Railway 部署的 PocketBase CMS**

- **技術棧：** PocketBase (Go-based headless CMS)
- **部署平台：** Railway
- **網域：** cms.taizanthebar.com
- **說明：** 無頭式內容管理系統，提供 API 給前端使用

**部署步驟：**
1. 推送程式碼到 GitHub
2. 在 Railway 建立新專案並連接儲存庫
3. 設定服務目錄為 `cms/`
4. 新增 Volume 並掛載到 `/pb/pb_data`
5. 設定自訂網域：cms.taizanthebar.com
6. 首次訪問後台建立管理員帳號
7. 配置 CORS 允許前端網域存取

## 開發環境設定

### 前端開發
```bash
cd frontend
npm install
npm run dev
```

### CMS 本地測試（使用 Docker）
```bash
cd cms
docker build -t personal-cms .
docker run -p 8080:8080 personal-cms
```

## 資料備份

### PocketBase 資料備份
- **重要：** 定期下載 `/pb/pb_data` 目錄（包含 SQLite 資料庫）
- **Railway Volume：** 確保資料持久化不會遺失
- **建議：** 設定自動備份到雲端儲存

## 環境變數

### Frontend (Vercel)
```env
VITE_API_URL=https://cms.taizanthebar.com
```

### CMS (Railway)
```env
PORT=8080  # Railway 自動注入
```

## 技術文件

- [Vue.js 文件](https://vuejs.org/)
- [Tailwind CSS 文件](https://tailwindcss.com/)
- [PocketBase 文件](https://pocketbase.io/docs/)
- [Vercel 部署指南](https://vercel.com/docs)
- [Railway 部署指南](https://docs.railway.app/)

## 授權

MIT License - 詳見 [LICENSE](cms/LICENSE) 檔案
