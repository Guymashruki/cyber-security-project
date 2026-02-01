import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css' // אם אין לך קובץ כזה, מחק את השורה הזו
import Dashboard from './Dashboard.jsx' // שים לב: אנחנו טוענים ישר את הדשבורד

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Dashboard />
  </StrictMode>,
)