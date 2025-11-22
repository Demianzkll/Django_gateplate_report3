from django.db import models

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'employees'
        verbose_name = 'Працівник'
        verbose_name_plural = 'Працівники'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    license_plate = models.CharField(max_length=10, unique=True)
    car_brand = models.CharField(max_length=15, null=True, blank=True)
    color = models.CharField(max_length=15, null=True, blank=True)
    car_image = models.CharField(max_length=255, null=True, blank=True)  
    car_status = models.CharField(max_length=10, null=True, blank=True)
    owner = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vehicles'
    )

    class Meta:
        db_table = 'vehicles'
        verbose_name = 'Автомобіль'
        verbose_name_plural = 'Автомобілі'

    def __str__(self):
        return f"{self.license_plate} ({self.car_brand})"


class AccessLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    datetime_entry = models.DateTimeField(null=True, blank=True)
    car_status = models.CharField(max_length=10, null=True, blank=True)
    image_url = models.URLField(max_length=255, null=True, blank=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='access_logs'
    )

    class Meta:
        db_table = 'accesslog'
        verbose_name = 'Журнал доступу'
        verbose_name_plural = 'Журнал доступу'

    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.car_status or 'N/A'}"
