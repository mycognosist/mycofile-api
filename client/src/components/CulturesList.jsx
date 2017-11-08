import React from 'react';
import { Table } from 'react-bootstrap';

const CulturesList = (props) => {
  return (
    <div>
      <h1>Culture Library</h1>
      <hr/><br/>
      <Table striped bordered condensed hover>
        <thead>
          <tr>
            <th>ID</th>
            <th>Culture ID</th>
            <th>Genus</th>
            <th>Species</th>
            <th>Strain</th>
            <th>Source</th>
          </tr>
        </thead>
        <tbody>
          {
            props.cultures.map((culture) => {
              return (
                <tr key={culture.id}>
                  <td>{culture.id}</td>
                  <td>{culture.culture_id}</td>
                  <td>{culture.genus}</td>
                  <td>{culture.species}</td>
                  <td>{culture.strain}</td>
                  <td>{culture.source}</td>
                </tr>
              )
            })
          }
        </tbody>
      </Table>
    </div>
  )
}

export default CulturesList;
