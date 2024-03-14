import { createBrowserRouter } from 'react-router-dom'

import MainPage from './pages/MainPage.tsx'
import StaffPage from './pages/StaffPage.tsx'

const status = 'staff'

const router = createBrowserRouter([
  {
    path: '/',
    element: status === 'staff' ? <StaffPage/> : <MainPage/>
  }
])


export default router