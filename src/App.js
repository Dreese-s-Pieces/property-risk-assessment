import React from 'react';
import './App.css';

export default App;

function App() {
  return (
    <div className="App">
      <header className="App-header">
        Property Risk Assessment
      </header>

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
