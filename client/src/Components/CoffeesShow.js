import React from 'react'
import { useParams } from 'react-router-dom'

function CoffeesShow() {

    const params = useParams()
  return (
    <div>CoffeesShow coffe number {params.id}</div>
  )
}

export default CoffeesShow