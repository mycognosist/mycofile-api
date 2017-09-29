import React from 'react';

const AddCulture = (props) => {
  return (
    <form onSubmit={(event) => props.addCulture(event)}>
      <div className="form-group">
        <input
          name="unique_id"
          className="form-control input-lg"
          type="text"
          placeholder="Unique ID"
          required
          value={props.unique_id}
          onChange={props.handleChange}
        />
      </div>
      <div className="form-group">
        <input
          name="genus"
          className="form-control input-lg"
          type="text"
          placeholder="Genus"
          required
          value={props.genus}
          onChange={props.handleChange}
        />
      </div>
      <div className="form-group">
        <input
          name="species"
          className="form-control input-lg"
          type="text"
          placeholder="Species"
          required
          value={props.species}
          onChange={props.handleChange}
        />
      </div>
      <div className="form-group">
        <input
          name="strain"
          className="form-control input-lg"
          type="text"
          placeholder="Strain"
          required
          value={props.strain}
          onChange={props.handleChange}
        />
      </div>
      <input
        type="submit"
        className="btn btn-primary btn-lg btn-block"
        value="Submit"
      />
    </form>
  )
}

export default AddCulture;
