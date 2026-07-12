function openModal(imageSrc, title, frames) {
            const modal = document.getElementById('modal');
            const modalContent = document.getElementById('modal-content');
            const modalImage = document.getElementById('modal-image');
            const modalTitle = document.getElementById('modal-title');
            const modalFrames = document.getElementById('modal-frames');
            
   
            modalImage.src = imageSrc;
            modalImage.alt = title;
            modalTitle.textContent = title;
            modalFrames.textContent = frames;
            
            modal.classList.remove('hidden');
            document.body.classList.add('modal-open');
            
            setTimeout(() => {
                modal.classList.add('opacity-100');
                modalContent.classList.remove('scale-90');
                modalContent.classList.add('scale-100');
            }, 10);
        }
        
        function closeModal() {
            const modal = document.getElementById('modal');
            const modalContent = document.getElementById('modal-content');
            
            modal.classList.remove('opacity-100');
            modalContent.classList.remove('scale-100');
            modalContent.classList.add('scale-90');
            
            setTimeout(() => {
                modal.classList.add('hidden');
                document.body.classList.remove('modal-open');
            }, 300);
        }
        
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeModal();
            }
        });