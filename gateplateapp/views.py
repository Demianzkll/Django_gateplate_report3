from django.conf import settings
from django.db.models import Max
from django.shortcuts import render
from django.views import View
from .models import Vehicle, AccessLog
from django.core.files.storage import default_storage
from .utils import PlateRecognizer                      



class HomeView(View):
    template_name = "pages/home.html"

    def get(self, request):
        return render(request, self.template_name)




class ResultView(View):
    template_name = "pages/result.html"
    tesseract_path = r"C:\Users\Demian\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    model_path = "best.pt"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        plate_number = None
        access_status = "denied"
        image_url = None
        message = None

        if request.FILES.get("car_image"):
            car_image = request.FILES["car_image"]

            file_path = default_storage.save("tmp/" + car_image.name, car_image)
            full_path = default_storage.path(file_path)
            image_url = "/media/" + file_path

            recognizer = PlateRecognizer(
                model_path=self.model_path,
                tesseract_path=self.tesseract_path
            )
            plate_number = recognizer.recognize_plate(full_path)

            if not plate_number or plate_number.strip().lower() in ["невпізнано", "не розпізнано"]:
                message = "Номер не розпізнано!"
            else:
                vehicle = Vehicle.objects.filter(license_plate=plate_number).first()
                if not vehicle:
                    message = f"Автомобіль {plate_number} не знайдено в базі!"
                else:
                    access_status = "allowed" if (vehicle.car_status or "").lower() == "дозволено" else "denied"
                    message = f"Автомобіль {plate_number} знайдено в базі."

        context = {
            "plate_number": plate_number,
            "access_status": access_status,
            "image_url": image_url,
            "message": message,
        }
        return render(request, self.template_name, context)



    




class VehiclesView(View):
    template_name = "pages/vehicles.html"

    def get(self, request):
        vehicles = Vehicle.objects.select_related("owner").all().order_by("license_plate")

        last_entries = (
            AccessLog.objects
            .values("vehicle_id")
            .annotate(last_date=Max("datetime_entry"))
        )
        last_log_dict = {entry["vehicle_id"]: entry["last_date"] for entry in last_entries}

        for v in vehicles:
            v.last_access = last_log_dict.get(v.vehicle_id)

        context = {
            "vehicles": vehicles,
            "MEDIA_URL": settings.MEDIA_URL,
        }
        return render(request, self.template_name, context)



