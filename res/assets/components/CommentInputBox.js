import PropTypes from 'prop-types';
import React from 'react';
import {lang} from '@pytsite/assetman';
import httpAPI from '@pytsite/http-api';


export default class CommentInputBox extends React.Component {
    static propTypes = {
        authenticationURL: PropTypes.string.isRequired,
        autoFocus: PropTypes.bool,
        className: PropTypes.string,
        isUserAllowedToComment: PropTypes.bool.isRequired,
        isUserAuthenticated: PropTypes.bool.isRequired,
        isVisible: PropTypes.bool,
        maxBodyLength: PropTypes.number.isRequired,
        minBodyLength: PropTypes.number.isRequired,
        onPost: PropTypes.func,
        parentUID: PropTypes.string,
        placeholder: PropTypes.string,
        postURL: PropTypes.string.isRequired,
        threadUID: PropTypes.string.isRequired,
    };

    static defaultProps = {
        autoFocus: false,
        className: 'input-box',
        isVisible: true,
        placeholder: lang.t('comments_odm@enter_your_comment'),
    };

    constructor(props) {
        super(props);

        this.state = {
            body: '',
            isPostingInProgress: false,
        };

        this.postComment = this.postComment.bind(this);
        this.onTextAreaChange = this.onTextAreaChange.bind(this);
    }

    onTextAreaChange(e) {
        this.setState({
            body: e.target.value
        });
    }

    postComment() {
        const args = {
            body: this.state.body,
            parent_uid: this.props.parentUID,
        };

        this.setState({isPostingInProgress: true});

        httpAPI.post(this.props.postURL, args).then(r => {
            this.props.onPost && this.props.onPost(r);
            this.setState({
                body: '',
                isPostingInProgress: false,
            });
        }).catch(e => {
            const error = e.responseJSON.error;
            if (error)
                alert(error);
            else
                console.error(e);
        })
    }

    render() {
        if (!this.props.isVisible)
            return null;

        let content;

        if (this.props.isUserAuthenticated) {
            if (this.props.isUserAllowedToComment) {
                content = (
                    <React.Fragment>
                    <textarea autoFocus={this.props.autoFocus}
                              disabled={this.state.isPostingInProgress}
                              maxLength={this.props.maxBodyLength}
                              minLength={this.props.minBodyLength}
                              onChange={this.onTextAreaChange}
                              placeholder={this.props.placeholder}
                              required={true}
                              value={this.state.body}
                    ></textarea>

                        <button disabled={(this.state.body.length < this.props.minBodyLength) || this.state.isPostingInProgress}
                                onClick={this.postComment}
                        >
                            {lang.t('comments_odm@post_comment')}
                        </button>
                    </React.Fragment>
                );
            } else {
                content = <p>{lang.t('comments_odm@no_permissions_to_create_comments')}</p>
            }
        } else {
            content = <a href={this.props.authenticationURL}>{lang.t('comments_odm@sign_in_to_post_comments')}</a>;
        }

        return (
            <div className={this.props.className}>
                {content}
            </div>
        );
    }
}
