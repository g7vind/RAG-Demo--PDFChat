css = '''
<style>
.chat-message {
    padding: 1.2rem;
    border-radius: 1rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.chat-message:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.25);
}
.chat-message.user {
    background: linear-gradient(135deg, #2b313e, #3d4455);
}
.chat-message.bot {
    background: linear-gradient(135deg, #475063, #5b6480);
}
.chat-message .avatar {
  width: 60px;
  height: 60px;
  flex-shrink: 0;
}
.chat-message .avatar img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #fff;
  box-shadow: 0 0 12px rgba(255,255,255,0.2);
  transition: transform 0.3s ease;
}
.chat-message .avatar img:hover {
  transform: rotate(5deg) scale(1.05);
}
.chat-message .message {
  flex: 1;
  margin-left: 1rem;
  font-size: 1rem;
  line-height: 1.5;
  color: #f1f1f1;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://img.icons8.com/fluency/96/robot-2.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://img.icons8.com/fluency/96/user-male-circle.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
