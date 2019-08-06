import './Comment.scss';

import PropTypes from 'prop-types';
import React from 'react';
import {lang} from '@pytsite/assetman';
import httpAPI from '@pytsite/http-api';
import CommentInputBox from '@pytsite/comments-odm/components/CommentInputBox';

export default class Comment extends React.Component {
    static propTypes = {
        authenticationURL: PropTypes.string.isRequired,
        className: PropTypes.string,
        data: PropTypes.shape({
            author: PropTypes.shape({
                name: PropTypes.string,
                picture_url: PropTypes.string,
            }),
            body: PropTypes.string,
            children: PropTypes.array,
            depth: PropTypes.number,
            is_new: PropTypes.bool,
            parent_uid: PropTypes.string,
            permissions: PropTypes.shape({
                delete: PropTypes.bool,
                modify: PropTypes.bool,
            }),
            publish_time: PropTypes.shape({
                ago: PropTypes.string,
                pretty_date: PropTypes.string,
                pretty_date_time: PropTypes.string,
                w3c: PropTypes.string,
            }),
            status: PropTypes.string,
            thread_uid: PropTypes.string,
            uid: PropTypes.string,
            urls: PropTypes.shape({
                delete: PropTypes.string,
                report: PropTypes.string,
            }),
        }).isRequired,
        isUserAuthenticated: PropTypes.bool.isRequired,
        onDelete: PropTypes.func.isRequired,
        onReply: PropTypes.func.isRequired,
        postURL: PropTypes.string.isRequired,
        settings: PropTypes.shape({
            maxBodyLength: PropTypes.number.isRequired,
            maxDepth: PropTypes.number.isRequired,
            minBodyLength: PropTypes.number.isRequired,
            permissions: PropTypes.shape({
                create: PropTypes.bool.isRequired,
            }).isRequired,
            statuses: PropTypes.object.isRequired,
        }).isRequired,
        threadUID: PropTypes.string.isRequired,
    };

    static defaultProps = {
        className: 'comment',
    };

    /**
     * Constructor
     *
     * @param props
     */
    constructor(props) {
        super(props);

        this.state = {
            isReplyBoxVisible: false,
        };

        this.onDeleteClick = this.onDeleteClick.bind(this);
        this.onReplyClick = this.onReplyClick.bind(this);
        this.onReplyPost = this.onReplyPost.bind(this);
        this.renderContentBlock = this.renderContentBlock.bind(this);
        this.renderChildrenBlock = this.renderChildrenBlock.bind(this);
        this.renderReplyBoxBlock = this.renderReplyBoxBlock.bind(this);
    }

    /**
     * Called after 'Delete' button clicked
     */
    onDeleteClick(e) {
        e.preventDefault();

        if (confirm(lang.t('comments_odm@confirm_comment_deletion'))) {
            this.setState({isReplyBoxVisible: false});
            httpAPI.del(this.props.data.urls.delete).then(() => {
                this.props.onDelete && this.props.onDelete(this.props.data.uid);
            });
        }
    }

    /**
     * Called after 'Reply' button clicked
     */
    onReplyClick(e) {
        e.preventDefault();

        // Show reply box
        this.setState({isReplyBoxVisible: !this.state.isReplyBoxVisible});
    }

    /**
     * Called after reply posted
     */
    onReplyPost(reply) {
        // Hide reply box
        this.setState({isReplyBoxVisible: false});

        // Notify outer listener
        this.props.onReply && this.props.onReply(reply);
    }

    /**
     * Renders content block
     */
    renderContentBlock() {
        let body;
        let className = `content ${this.props.data.status}`;

        if (this.props.data.status === 'published')
            body = this.props.data.body;
        else if (this.props.data.status === 'deleted')
            body = lang.t('comments_odm@comment_deleted');
        else if (this.props.data.status === 'spam')
            body = lang.t('comments_odm@spam_comment');

        return <div className={className}>
            <div className="l">
                <img src={this.props.data.author.picture_url} alt={this.props.data.author.name}/>
            </div>
            <div className="r">
                <div className="header">
                    <div className="author">{this.props.data.author.name}</div>

                    <div className="publish-time" title={this.props.data.publish_time.pretty_date_time}>
                        {this.props.data.publish_time.ago}
                    </div>
                </div>

                <div className="body">{body}</div>

                <div className="footer">
                    {this.props.data.status === 'published' && this.props.data.depth < this.props.settings.maxDepth && (
                        <a href="#" className="action-reply" onClick={this.onReplyClick}>
                            {lang.t('comments_odm@reply')}
                        </a>
                    )}

                    {(this.props.data.status === 'published' && this.props.data.permissions.delete) && (
                        <a href="#" className="action delete" onClick={this.onDeleteClick}>
                            {lang.t('comments_odm@delete')}
                        </a>
                    )}
                </div>
            </div>
        </div>
    }

    /**
     * Renders children block
     */
    renderChildrenBlock() {
        return <div className="children">
            {this.props.data.children.map((child, index) => {
                return <Comment authenticationURL={this.props.authenticationURL}
                                data={child}
                                isUserAuthenticated={this.props.isUserAuthenticated}
                                key={index}
                                onDelete={this.props.onDelete}
                                onReply={this.props.onReply}
                                postURL={this.props.postURL}
                                settings={this.props.settings}
                                threadUID={this.props.threadUID}
                />
            })}
        </div>
    }

    /**
     * Renders reply box
     */
    renderReplyBoxBlock() {
        return <CommentInputBox authenticationURL={this.props.authenticationURL}
                                autoFocus={this.props.data.uid !== null}
                                isUserAllowedToComment={this.props.settings.permissions.create}
                                isUserAuthenticated={this.props.isUserAuthenticated}
                                maxBodyLength={this.props.settings.maxBodyLength}
                                minBodyLength={this.props.settings.minBodyLength}
                                onPost={this.onReplyPost}
                                parentUID={this.props.data.uid}
                                postURL={this.props.postURL}
                                threadUID={this.props.threadUID}
                                isVisible={this.props.data.uid === null || this.state.isReplyBoxVisible}
        />
    }

    /**
     * Renders component
     */
    render() {
        let addClass = '' + (this.props.data.is_new ? ' new': '');

        return (
            <div className={this.props.className + addClass} id={`pytsite-comment-${this.props.data.uid}`}>
                {this.props.data.uid && this.renderContentBlock()}
                {this.renderReplyBoxBlock()}
                {this.props.data.children && this.renderChildrenBlock()}
            </div>
        )
    }
}
