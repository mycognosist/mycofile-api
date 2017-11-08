import React from 'react';

const CulturesList = (props) => {
  return (
    <div>
      {
        props.cultures.map((culture) => {
          return <h4 key={culture.id} className="well"><strong>{culture.culture_id}</strong> | <em>{culture.genus} {culture.species}</em> '{culture.strain}'</h4>
        })
      }
    </div>
  )
}

export default CulturesList;
