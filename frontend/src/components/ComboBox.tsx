import TextField from '@mui/material/TextField'
import Autocomplete from '@mui/material/Autocomplete'
import { useEffect, useState } from 'react'
import axios from 'axios'

export default function ComboBox() {
  const [data, setData] = useState()

  const getData = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/agents/')
      setData(res.data.data)
    } catch (error) {
      console.error(error)
    }
  }

  useEffect(() => {
    getData()
  }, [])
  // @ts-ignore
  const newData = data?.map(d => d.title)

  return (
    <>
      {data && (
        <Autocomplete
          disablePortal
          id="combo-box-demo"
          options={ newData }
          sx={ { width: 300 } }
          renderInput={ (params) => <TextField { ...params } label="Agents"/> }
        />
      )}
      {!data && (
        <div>
          loading
        </div>
      )}
    </>
  )
}
