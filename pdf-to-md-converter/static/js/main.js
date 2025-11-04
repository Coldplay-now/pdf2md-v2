// PDF to Markdown Converter - 前端脚本

const API_BASE = '';
let currentTaskId = null;
let pollInterval = null;

// DOM元素
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const uploadBtn = document.getElementById('uploadBtn');
const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressMessage = document.getElementById('progressMessage');
const resultSection = document.getElementById('resultSection');
const errorMessage = document.getElementById('errorMessage');

// 拖拽上传
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

uploadArea.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

// 处理文件选择
function handleFileSelect(file) {
    if (!file.name.endsWith('.pdf')) {
        showError('请选择PDF文件！');
        return;
    }
    
    // 显示文件信息
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    fileInfo.classList.remove('hidden');
    uploadBtn.disabled = false;
    
    // 存储文件
    fileInput.files = createFileList(file);
}

// 创建FileList
function createFileList(file) {
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    return dataTransfer.files;
}

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

// 上传并处理
uploadBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) {
        showError('请先选择文件！');
        return;
    }
    
    uploadBtn.disabled = true;
    hideError();
    showProgress();
    
    try {
        // 上传文件
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${API_BASE}/api/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('上传失败');
        }
        
        const data = await response.json();
        currentTaskId = data.task_id;
        
        // 开始轮询任务状态
        startPolling();
        
    } catch (error) {
        showError('上传失败: ' + error.message);
        uploadBtn.disabled = false;
        hideProgress();
    }
});

// 开始轮询任务状态
function startPolling() {
    if (pollInterval) {
        clearInterval(pollInterval);
    }
    
    pollInterval = setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE}/api/status/${currentTaskId}`);
            if (!response.ok) {
                throw new Error('查询状态失败');
            }
            
            const data = await response.json();
            updateProgress(data);
            
            // 任务完成或失败时停止轮询
            if (data.status === 'completed') {
                clearInterval(pollInterval);
                showResult(data);
            } else if (data.status === 'failed') {
                clearInterval(pollInterval);
                showError('处理失败: ' + data.message);
                hideProgress();
                uploadBtn.disabled = false;
            }
            
        } catch (error) {
            console.error('轮询错误:', error);
        }
    }, 1000); // 每秒查询一次
}

// 更新进度
function updateProgress(data) {
    const progress = data.progress || 0;
    progressFill.style.width = progress + '%';
    progressFill.textContent = progress + '%';
    progressMessage.textContent = data.message || '处理中...';
    
    // 更新日志
    if (data.logs) {
        const logContainer = document.getElementById('logContainer');
        
        if (data.logs.length > 0) {
            logContainer.innerHTML = '';
            
            data.logs.forEach(log => {
                const logEntry = document.createElement('div');
                logEntry.className = 'log-entry';
                logEntry.textContent = log;
                logContainer.appendChild(logEntry);
            });
            
            // 自动滚动到底部
            logContainer.scrollTop = logContainer.scrollHeight;
        }
    }
}

// 显示结果
function showResult(data) {
    hideProgress();
    resultSection.classList.remove('hidden');
    
    const result = data.result;
    const summary = result.summary;
    
    // 更新统计信息
    document.getElementById('totalPages').textContent = summary.total_pages;
    document.getElementById('successPages').textContent = summary.successful_pages;
    document.getElementById('totalChars').textContent = summary.total_characters.toLocaleString();
    document.getElementById('successRate').textContent = summary.success_rate;
    
    // 设置下载按钮
    document.getElementById('downloadMd').onclick = () => {
        window.location.href = `${API_BASE}/api/download/${currentTaskId}/markdown`;
    };
    
    // 加载Markdown预览
    loadMarkdownPreview(currentTaskId);
    
    // 重置上传按钮
    uploadBtn.disabled = false;
}

// 加载Markdown预览
async function loadMarkdownPreview(taskId) {
    try {
        const response = await fetch(`${API_BASE}/api/download/${taskId}/markdown`);
        if (response.ok) {
            const text = await response.text();
            const preview = document.getElementById('markdownPreview');
            preview.textContent = text.substring(0, 2000) + (text.length > 2000 ? '\n\n... (预览前2000字符)' : '');
        }
    } catch (error) {
        console.error('加载预览失败:', error);
    }
}

// 显示/隐藏进度
function showProgress() {
    progressSection.classList.remove('hidden');
    progressFill.style.width = '0%';
    progressFill.textContent = '0%';
    
    // 清空日志
    const logContainer = document.getElementById('logContainer');
    logContainer.innerHTML = '<div class="log-entry">等待开始...</div>';
}

function hideProgress() {
    progressSection.classList.add('hidden');
}

// 显示/隐藏错误
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
}

function hideError() {
    errorMessage.classList.add('hidden');
}

// 页面加载完成
document.addEventListener('DOMContentLoaded', () => {
    console.log('PDF to Markdown Converter - 已就绪');
    
    // 检查服务健康状态
    fetch(`${API_BASE}/api/health`)
        .then(res => res.json())
        .then(data => {
            console.log('服务状态:', data);
        })
        .catch(err => {
            console.error('服务连接失败:', err);
            showError('无法连接到服务器，请检查服务是否启动');
        });
});

