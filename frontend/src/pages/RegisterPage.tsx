import { Box, Button, TextField } from '@mui/material'
import { useEffect, useState } from 'react'
import axiosInstance from '../api'
import Cookies from 'js-cookie'
import { useNavigate } from 'react-router-dom'

const RegisterPage = () => {
  const [username, setUsername] = useState<string>('')
  const [password, setPassword] = useState<string>('')

  const navigate = useNavigate()

  //   api/fullAccess/
  // api/privateAccess/

  const handleFull = async () => {
    const res = await axiosInstance.get('/fullAccess/')
    const res2 = await axiosInstance.post('/fullAccess/')
    console.log(res)
    console.log(res2)
  }

  const handlePrivate = async () => {
    const res = await axiosInstance.get('/privateAccess/')
    const res2 = await axiosInstance.post('/privateAccess/')
    console.log(res)
    console.log(res2)
  }

  const handleSubmit = async () => {
    const res = await axiosInstance.post('/user/register/', {
      username: username,
      password: password
    })
    console.log(res.status)

    if (res.status === 200 || res.status === 201) {
      const res = await axiosInstance.post('/token/', {
        username: username,
        password: password
      })
      console.log('privet',res)

      Cookies.set('access_token', res.data.access, { path: '/' })
      Cookies.set('refresh_token', res.data.refresh, { path: '/' })

      navigate('/')
    }

    console.log(res)
  }

  useEffect(() => {})

  return (
    <>
      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
        <TextField
          value={username}
          onChange={e => setUsername(e.target.value)}
          name="username"
          label="Имя пользователя"
          type="string"
          variant="standard"
        />
        <TextField
          value={password}
          onChange={e => setPassword(e.target.value)}
          name="password"
          label="Пароль"
          type="string"
          variant="standard"
        />
        <Button onClick={handleSubmit}>Отправить</Button>

        <Button onClick={handleFull}>Full</Button>
        <Button onClick={handlePrivate}>Private</Button>
      </Box>
    </>
  )
}

export default RegisterPage
