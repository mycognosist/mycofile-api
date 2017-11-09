import React from 'react';

const AddLineObject = (props) => {
  return (
    <form onSubmit={(event) => props.addLineObject(event)}>
      <div className="form-group">
        <input
          name="culture_id"
          className="form-control input-lg"
          type="text"
          placeholder="Culture ID"
          required
          value={props.culture_id}
          onChange={props.handleChange}
        />
      </div>
      <div className="form-group">
        <input
          name="container"
          className="form-control input-lg"
          type="text"
          placeholder="Container"
          required
          value={props.container}
          onChange={props.handleChange}
        />
      </div>
      <div className="form-group">
        <input
          name="dimensions"
          className="form-control input-lg"
          type="text"
          placeholder="Dimensions"
          required
          value={props.dimensions}
          onChange={props.handleChange}
        />
      </div>
      <div className="form-group">
        <input
          name="substrate"
          className="form-control input-lg"
          type="text"
          placeholder="Substrate"
          required
          value={props.substrate}
          onChange={props.handleChange}
        />
      </div>
      <div className="form-group">
        <input
          name="treatment"
          className="form-control input-lg"
          type="text"
          placeholder="Treatment"
          required
          value={props.treatment}
          onChange={props.handleChange}
        />
      </div>
      <div className="form-group">
        <input
          name="duration"
          className="form-control input-lg"
          type="text"
          placeholder="Duration"
          required
          value={props.duration}
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

export default AddLineObject;
