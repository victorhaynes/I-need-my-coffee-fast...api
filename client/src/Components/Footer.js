import React from 'react'
import { Container } from 'react-bootstrap'

function Footer() {
  return (
    <footer class ="py-5 my-5 bg-dark">
        <Container className='px-4'>
            <p class="text-center text-white">
                Copyright &copy; I Need My Coffee Fast...API - 2023
            </p>
            <p class="text-center text-white">
                <a style={{color: "white"}} href='https://github.com/victorhaynes/I-need-my-coffee-fast...api'>A project by Victor Haynes </a>
            </p>
            
        </Container>
    </footer>
    )
}

export default Footer