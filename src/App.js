import React, { useState, useEffect } from 'react';
import './App.css';

export default App;

function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      console.log(data);
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        Property Risk Assessment
      </header>
      <div className='row-container'>
        <div className='address-form'>
          <AddressForm/>
        </div>

        <div className='display-container'>
          <p>{currentTime}</p>

          <Display/>

        </div>
      </div>
    </div>
  );
}

class AddressForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      street_address: '',
      city: '',
      state: '',
      zip_code: ''
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  } 
  
  handleSubmit(event) {
    alert('Searching for address: ' + this.state.street_address);
    event.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        {/* <label>
          Address: 
          <textarea value={this.state.value} onChange={this.handleChange} />
        </label> */}
        <input className="address-input"
          name={"street_address"}
          value={this.state.street_address}
          placeholder={"Enter street address"}
          onChange={this.handleChange}
        />
        <br/>
        <input className="address-input"
          name={"city"}
          value={this.state.city}
          placeholder={"Enter city"}
          onChange={this.handleChange}
        />
        <br/>

        <input className="address-input"
          name={"state"}
          value={this.state.state}
          placeholder={"Enter state"}
          onChange={this.handleChange}
        />
        <br/>

        <input className="address-input"
          name={"zip_code"}
          value={this.state.zip_code}
          placeholder={"Enter zip code"}
          onChange={this.handleChange}
        />
        <br/>
        <input className="address-input"
          type="submit" 
          value="Submit"
        />
      </form>
    );
  }
}

class Display extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <p>This is the display</p>
    );
  }
}
