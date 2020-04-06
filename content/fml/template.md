Title: My super title
Date: 2019-08-26 18:20
Modified: 2019-08-26 18:20
Category: Python
Tags: pelican, publishing
Slug: Xiaomi-gtx-dsdt
Status: draft
Authors: Alexis Metaireau, Conan Doyle
Summary: Short version for index and feeds





_BIF函数(Battery Information)返回电池信息，在电池再次充电之前，这个信息是不变的。 返回值是一个package，数值域定义为

```c
Package { 
  Power Unit // Integer (DWORD) 
  Design Capacity // Integer (DWORD) 
  Last Full Charge Capacity // Integer (DWORD) 
  Battery Technology // Integer (DWORD) 
  Design Voltage // Integer (DWORD) 
  Design Capacity of Warning // Integer (DWORD) 
  Design Capacity of Low // Integer (DWORD) 
  Battery Capacity Granularity 1 // Integer (DWORD) 
  Battery Capacity Granularity 2 // Integer (DWORD) 
  Model Number // String (ASCIIZ) 
  Serial Number // String (ASCIIZ) 
  Battery Type // String (ASCIIZ) 
  OEM Information // String (ASCIIZ)
}
```



每个域的具体说明如下

| Field                          | Format | **Description**                                              |
| ------------------------------ | ------ | ------------------------------------------------------------ |
| Power Unit                     |        | 电池容量的信息<br>0x00000000则容量为[mWh]<br>0x00000001则容量为[mAh] |
| Design Capacity                |        | 设计容量<br>0xFFFFFFFF – Unknown design capacity             |
| Last Full Charge Capacity      |        | Predicted battery capacity when fully charged. The *Last Full Charge Capacity* value is expressed as power (mWh) or current (mAh) depending on the *Power Unit* value.<br> 0x000000000h – 0x7FFFFFFF (in [mWh] or [mAh] )<br>0xFFFFFFFF – Unknown last full charge capacity |
| Battery Technology             |        | 0x00000000 – Primary (for example, non-rechargeable)<br>0x00000001 – Secondary (for example, rechargeable) |
| Design Voltage                 |        | Nominal voltage of a new battery. <br>0x000000000 – 0x7FFFFFFF in [mV]<br>0xFFFFFFFF – Unknown design voltage. |
| Design capacity of Warning     |        | OEM-designed battery warning capacity.<br> “Low Battery Levels.” 0x000000000 – 0x7FFFFFFF in [mWh] or [mAh] |
| Design Capacity of Low         |        |                                                              |
| Battery Capacity Granularity 1 |        |                                                              |
| Battery Capacity Granularity 2 |        |                                                              |
| Model Number                   |        |                                                              |
| Serial Number                  |        |                                                              |
| Battery Type                   |        |                                                              |
| OEM Information                |        |                                                              |
|                                |        |                                                              |







```c
Package {
  Battery State // Integer (DWORD)
  Battery Present Rate // Integer (DWORD)
  Battery Remaining Capacity // Integer (DWORD)
  Battery Present Voltage // Integer (DWORD)
}
```

