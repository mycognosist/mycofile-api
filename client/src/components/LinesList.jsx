import React from 'react';

const LinesList = (props) => {
  return (
    <div>
      <h1>Lines</h1>
      <hr/><br/>
      <div>
        {
          props.lines.map((line) => {
            return (
              <div>
                <p>{line.indent}{line.culture_id}, {line.container}, {line.substrate}</p>
              </div>
            )
          })
        }
      </div>
    </div>
  )
};

export default LinesList;
