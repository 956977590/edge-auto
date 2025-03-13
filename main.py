from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.select import Select 
from selenium.webdriver.common.action_chains import ActionChains 
import configparser, random, time, os 
 
# 初始化配置 
config = configparser.ConfigParser()
config.read('config.ini')
 
class 智能打卡系统:
    def __init__(self):
        # 防封浏览器配置 
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        self.options.add_argument("--no-sandbox")  # Doprax专用参数 
       if config['浏览器设置']['类型'] == 'firefox':  
    self.driver = webdriver.Firefox(options=self.options)  
elif config['浏览器设置']['类型'] == 'edge':  
    self.driver = webdriver.Edge(options=self.options)
        self.driver.implicitly_wait(15)  # 延长等待时间 
 
    def 真人行为模拟(self):
        """模仿人类操作特征"""
        # 随机延迟（1.2±0.5秒）
        time.sleep(float(config['防封设置']['延迟时间']) + random.uniform(-0.5, 0.5))
        # 多维度滚动 
        for _ in range(int(config['防封设置']['滚动次数'])):
            self.driver.execute_script(f"window.scrollBy(0, {random.randint(400,800)})")
            time.sleep(0.5)
 
    def 处理通用字段(self):
        """填写所有表单的共性字段"""
        try:
            # 新版姓名字段（2025新增）
            self.driver.find_element(By.XPATH, "//input[contains(@name,'姓名')]").send_keys(config['个人信息']['姓名'])
        except: pass 
        
        # 必填工号与部门 
        self.driver.find_element(By.XPATH, "//input[contains(@placeholder,'工号')]").send_keys(config['基础信息']['工号'])
        Select(self.driver.find_element(By.XPATH, "//select[contains(@name,'部门')]")).select_by_visible_text(config['基础信息']['部门'])
 
    def 智能识别表单(self):
        """判断三种表单类型并处理"""
        # 类型1：带打分 
        if "请您来打分" in self.driver.page_source:
            Select(self.driver.find_element(By.XPATH, "//select[contains(@name,'打分')]")).select_by_index(random.randint(0,4))
        
        # 类型3：带班组长和政治面貌 
        elif "班组长" in self.driver.page_source:
            self.driver.find_element(By.XPATH, "//input[contains(@name,'班组长')]").send_keys(config['基础信息']['班组长'])
            政治面貌选择 = Select(self.driver.find_element(By.XPATH, "//select[contains(@name,'政治面貌')]"))
            政治面貌选择.select_by_visible_text(config['个人信息']['政治面貌'])
            self.自动答题模块()
        
        # 类型2：仅基础信息（无需额外操作）
 
    def 自动答题模块(self):
        """DeepSeek智能答题"""
        from deepseek_api import Chat 
        client = Chat(api_key=config['DeepSeek']['api_key'])
        
        # 获取所有题目 
        for question in self.driver.find_elements(By.CLASS_NAME, "question"):
            题目文本 = question.find_element(By.CLASS_NAME, "title").text 
            选项 = [opt.text for opt in question.find_elements(By.CLASS_NAME, "option")]
            
            # 调用API（加强多选提示）
            resp = client.create(
                model="deepseek-chat",
                messages=[{
                    "role": "user", 
                    "content": f"请回答：{题目文本}（选项：{'/'.join(选项)}）{'注意本题可能是多选' if '多选' in question.text else ''}"
                }]
            )
            
            # 执行点击操作 
            答案 = resp.choices[0].message.content 
            for opt in question.find_elements(ByL.CASS_NAME, "option               "):
 if any(key in opt.text for key in 答案.split()):
                    opt.click()
                    self.真人行为模拟()  # 选项间增加随机间隔 
 
    def 执行主流程(self):
        """全自动化控制中枢"""
        try:
            self.driver.get(os.getenv('公众号链接'))  # 从环境变量读取 
            
            # 首次扫码登录 
            if "login" in self.driver.current_url:
                input("请扫码登录后按回车继续...")
                self.driver.get(os.getenv('公众号链接'))  # 重新加载 
            
            # 遍历文章 
            for 文章 in self.driver.find_elements(By.CSS_SELECTOR, ".article:not(.转载)"):
                文章.click()
                self.真人行为模拟()
                
                try:
                    self.driver.find_element(By.LINK_TEXT, "阅读全文").click()
                    self.处理通用字段()
                    self.智能识别表单()
                    self.driver.find_element(By.XPATH, "//button[text()='提交']").click()
                    print(f"✅ 成功提交：{self.driver.title}")
                except Exception as e:
                    print(f"⚠️ 异常跳过：{str(e)}")
                finally:
                    self.driver.back()
        
        finally:
            self.driver.quit()
 
if __name__ == "__main__":
    智能打卡系统().执行主流程()