import React, { useState, useEffect } from 'react';
import './App.css';

export default App;

function App() {
  // const [currentTime, setCurrentTime] = useState(0);

  // useEffect(() => {
  //   fetch('/time').then(res => res.json()).then(data => {
  //     console.log(data);
  //     setCurrentTime(data.time);
  //   });
  // }, []);

  return (
    <div className="App">
      <header className="App-header">
        Property Risk Assessment
      </header>
      {/* <p>{currentTime}</p> */}

      <AddressForm/>
    </div>
  );
}

class AddressForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: 'Enter Address'
    };
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  } 
  
  handleSubmit(event) {
    alert('Searching for address: ' + this.state.value);
    event.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Address: 
          <textarea value={this.state.value} onChange={this.handleChange} />
        </label>
        <input type="submit" value="Submit"/>
      </form>
    );
  }
}
