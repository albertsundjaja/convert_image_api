import React, {Component} from 'react';

import {Container, Row, Col} from 'react-bootstrap';
import axios from 'axios';


class MainContainer extends Component {

    state = {
        'file':'',
        'errorMsg':'',
        'convertedFilename':'',
        'convertedFile':''
    }

    handleImageChosen = (e) => {
        const file = e.target.files[0];
        this.setState({
            'file':file
        })
    }

    convertImage = () => {
        let self = this;

        const file = this.state.file;
        let formData = new FormData();
        formData.append('file', file);
        let config = {
            header: {
                'Content-Type': 'multipart/form-data'
            }
        }
        axios.post('http://localhost:5000/upload_file', formData, config)
        .then((resp) => {
            console.log(resp);
            self.setState({
                errorMsg: '',
                convertedFilename: resp.data.filename
            })
        })
        .catch((err) => {
            console.log(err.response);
            self.setState({
                errorMsg: err.response.data.error
            })
        })
    }

    render() {
        const redStyle = {
            color:"red"
        }

        let err = (<div></div>);
        if (this.state.errorMsg !== '') {
            err = (
                <div>
                    {this.state.errorMsg}
                </div>
            )
        }

        let img = (<div></div>);
        if (this.state.convertedFilename!== '') {
            let url = 'http://localhost:5000/download_file/' + this.state.convertedFilename;
            img = (
                <img src={url}></img>
            )
        }
        return (
            <div>
                <Container>
                    <Row>
                        <Col xs="12">
                            <h1>RGB to Grayscale Converter</h1>
                        </Col>
                    </Row>
                    <Row>
                        <Col xs="12" md="6">
                            <h2>Choose Image</h2>
                            <label>Please only upload image with .png .jpg or .jpeg extension</label>
                            <input type="file" onChange={this.handleImageChosen} />
                            <button onClick={this.convertImage}>Convert</button>
                        </Col>
                    </Row>
                    <Row>
                        <Col xs="12" md="6">
                            <span style={redStyle}>{err}</span>
                        </Col>
                    </Row>
                    <Row>
                        <Col xs="12">
                            {img}
                        </Col>
                    </Row>
                </Container>
            </div>
        )
    }
}

export default MainContainer;