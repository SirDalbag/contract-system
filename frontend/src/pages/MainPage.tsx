import TableComponent from '../components/TableComponent.tsx'
import ContractForm from '../components/ContractForm.tsx'
import { Box } from '@mui/material'

const MainPage = () => {

  return (
    <>
      <Box
        sx={ { display: 'flex', justifyContent: 'center', flexDirection: 'column', alignItems: 'center', gap: '5px' } }>
        <TableComponent/>
        <ContractForm/>
      </Box>
    </>
  )
}

export default MainPage