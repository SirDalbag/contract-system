import TableComponent from '../components/TableComponent.tsx'
import ContractForm from '../components/ContractForm.tsx'
import { Box } from '@mui/material'
import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { IData, IForm } from '../schemas/IData.ts'
import { isDebug } from '../../constants.tsx'


const MainPage = () => {
  const [data, setData] = useState<IData[]>([])
  const [totalSum, setTotalSum] = useState<number>(0)
  const [form, setForm] = useState<IForm>({
    bin: '',
    comment: '',
    total: 0,
    file_path: null
  })
  const [fileSize, setFileSize] = useState<number>(0)

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target
    setForm({ ...form, [name]: value })
  }

  const getData = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/contracts/')
      setData(res.data.data)
    } catch (error) {
      if (isDebug) {
        console.error(`Error: ${ error }`)
      }
    }
  }

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files && event.target.files[0]

    if (file) {
      const fileSizeInBytes = file.size
      const fileSizeInKB = fileSizeInBytes / 1024
      setFileSize(fileSizeInKB)
      setForm({ ...form, file_path: file || null })
    } else {
      setFileSize(0)
    }
  }

  const postData = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    const formData = new FormData()
    formData.append('bin', 'BIN')
    formData.append('comment', form.comment)
    formData.append('total', form.total.toString())
    if (form.file_path) {
      formData.append('file_path', form.file_path)
    } else {
      window.alert('Choose a file')
      return
    }

    try {
      const res = await axios.post(
        'http://127.0.0.1:8000/api/contract/',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      )
      getData()
      if (isDebug) {
        console.log(res)
      }
    } catch (error) {
      if (isDebug) {
        console.error(`Error: ${ error }`)
      }
    }
  }

  useEffect(() => {
    getData()
  }, [])

  useEffect(() => {
    if (data) {
      setTotalSum(data.reduce((accumulator, row) => accumulator + parseFloat(row.total), 0))
    }
  }, [data])

  return (
    <>
      <Box
        sx={ { display: 'flex', justifyContent: 'center', flexDirection: 'column', alignItems: 'center', gap: '5px' } }>
        <TableComponent data={ data } totalSum={ totalSum }/>
        <ContractForm postData={ postData } handleFileChange={ handleFileChange } form={ form }
                      handleInputChange={ handleInputChange } fileSize={ fileSize }/>
      </Box>
    </>
  )
}

export default MainPage