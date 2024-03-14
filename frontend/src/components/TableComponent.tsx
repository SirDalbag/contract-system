import axios from 'axios'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Paper from '@mui/material/Paper'

import { useEffect, useState } from 'react'
import { Box } from '@mui/material'

interface IData {
  id: number
  total: string
  date: string
  file_path: string
  author: number
  agent_id: number
  comment_id: number
  username: string
}

const TableComponent = () => {
  const [data, setData] = useState<IData[]>([])
  const [totalSum, setTotalSum] = useState<number>(0)

  const getData = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/contracts/')
      setData(res.data.data)
    } catch (error) {
      console.error(`Error: ${error}`)
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
      <TableContainer component={ Paper }>
        <Table sx={ { minWidth: 650 } } aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell align="right">Date created</TableCell>
              <TableCell align="right">Price</TableCell>
              <TableCell align="right">File</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            { data.map((row) => (
              <TableRow
                key={ row.id }
                sx={ { '&:last-child td, &:last-child th': { border: 0 } } }
              >
                <TableCell component="th" scope="row">
                  { row.username }
                </TableCell>
                <TableCell align="right">{ row.date }</TableCell>
                <TableCell align="right">{ parseFloat(row.total) }</TableCell>
                <TableCell align="right"><a href={ `/static/${ row.file_path }` }>File</a></TableCell>
              </TableRow>
            )) }
          </TableBody>
        </Table>
      </TableContainer>
      <Box sx={{alignSelf: 'end'}}>Total: { totalSum }</Box>
    </>
  )
}

export default TableComponent