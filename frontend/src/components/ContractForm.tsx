import TextField from '@mui/material/TextField'
import ComboBox from './ComboBox.tsx'
import { Box, Button } from '@mui/material'
import React, { useState } from 'react'
import axios from 'axios'

interface IForm {
  comment: string
  total: number
  contract: string
  file_path: File | null
  date: string
}

const ContractForm = () => {
  const [form, setForm] = useState<IForm>({
    comment: '',
    total: 0,
    contract: '',
    file_path: null,
    date: ''
  })
  const [fileSize, setFileSize] = useState<number>(0)
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target
    setForm({ ...form, [name]: value })
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
    formData.append('comment', form.comment)
    formData.append('total', form.total.toString())
    formData.append('contract', form.contract)
    formData.append('agent_title', "AGentO")
    formData.append('date', new Date().toISOString().split('T')[0])
    if (form.file_path) {
      formData.append('file_path', form.file_path)

    } else {
      window.alert('Choose a file')
      return
    }

    try {
      const res = await axios.post('http://127.0.0.1:8000/api/contract/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      // props.updateData()
      // console.log(onUpdateData)
      console.log(res)
    } catch (error) {
      console.error(`Error: ${ error }`)
    }
  }

  return (
    <>
      <form onSubmit={ postData }>
        <Box sx={ { display: 'flex', flexDirection: 'column', gap: '5px', width: '200px' } }>
          <ComboBox/>
          <Button variant="contained" component="label">
            Upload File
            <input onChange={ handleFileChange } type="file" name="file_path" hidden/>
          </Button> { form.file_path ? form.file_path.name : '' }

          <TextField value={ form.comment }
                     onChange={ handleInputChange }
                     name="comment"
                     label="Comment"
                     variant="standard"/>
          <TextField value={ form.total }
                     onChange={ handleInputChange }
                     name="total"
                     label="Total"
                     type="number"
                     variant="standard"/>
          { fileSize < 10 * 1024 ? (
            <Button type="submit">Submit</Button>
          ) : (
            <Button disabled type="submit">Submit</Button>
          )
          }
        </Box>
      </form>
    </>
  )
}

export default ContractForm
